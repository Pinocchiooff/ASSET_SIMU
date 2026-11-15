#!/usr/bin/env python3
"""Fetch known public source files and safely stage archives for asset review."""
from __future__ import annotations

import hashlib
import json
import shutil
import urllib.error
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

OWNER = "Pinocchiooff"
REPO = "aeroesiee-ai-studio"
REF = "main"
ROOT = Path(__file__).resolve().parents[1]
ARCHIVES = ROOT / "source-assets" / "archives"
EXTRACTED = ROOT / "source-assets" / "extracted"

FILES = [
    "aerial_asphalt_01_1k.gltf.zip",
    "aerial_grass_rock_1k.gltf.zip",
    "aerial_rocks_04_2k.gltf.zip",
    "asphalt_02_2k.gltf.zip",
    "autumn_field_puresky_4k.hdr",
    "bark_willow_1k.gltf.zip",
    "brown_mud_02_1k.gltf.zip",
    "brown_mud_leaves_01_2k.gltf.zip",
    "brushed_concrete_04_1k.gltf.zip",
    "coast_rocks_02_diff_1k.jpg",
    "coast_rocks_02_nor_gl_1k.exr",
    "coast_rocks_02_rough_1k.exr",
    "coast_sand_04_1k.gltf.zip",
    "coast_sand_rocks_02_2k.gltf.zip",
    "concrete_road_barrier_2k.blend.zip",
    "corrugated_iron_02_1k.gltf.zip",
    "covered_car_2k.blend.zip",
    "exterior_aircon_unit_01_diff_2k.png",
    "exterior_aircon_unit_01_metal_2k.png",
    "exterior_aircon_unit_01_nor_gl_2k.png",
    "exterior_aircon_unit_01_opacity_2k.png",
    "exterior_aircon_unit_01_rough_2k.png",
    "exterior_aircon_unit_02_diff_2k.png",
    "exterior_aircon_unit_02_metal_2k.png",
    "exterior_aircon_unit_02_nor_gl_2k.png",
    "exterior_aircon_unit_02_rough_2k.png",
    "exterior_aircon_unit_2k.blend",
    "exterior_aircon_unit_rusted_01_diff_2k.png",
    "exterior_aircon_unit_rusted_01_metal_2k.png",
    "exterior_aircon_unit_rusted_01_nor_gl_2k.png",
    "exterior_aircon_unit_rusted_01_rough_2k.png",
    "exterior_aircon_unit_rusted_02_diff_2k.png",
    "exterior_aircon_unit_rusted_02_metal_2k.png",
    "venice_sunset_4k.hdr",
    "weathered_plank_siding_1k.gltf.zip",
    "wood_inlaid_stone_wall_1k.gltf.zip",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_extract(archive: Path, destination: Path) -> None:
    """Extract ZIP members only when their resolved path stays in destination."""
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()
    with zipfile.ZipFile(archive) as zf:
        for member in zf.infolist():
            name = member.filename.replace("\\", "/")
            relative = PurePosixPath(name)
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError(f"Unsafe ZIP member rejected: {member.filename}")
            target = (destination / Path(*relative.parts)).resolve()
            if target != root and root not in target.parents:
                raise ValueError(f"ZIP member escapes destination: {member.filename}")
            if member.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(member) as source, target.open("wb") as output:
                shutil.copyfileobj(source, output)


def main() -> int:
    ARCHIVES.mkdir(parents=True, exist_ok=True)
    EXTRACTED.mkdir(parents=True, exist_ok=True)
    raw_base = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{REF}/"
    seen_hashes: dict[str, str] = {}
    failures = 0

    for filename in FILES:
        target = ARCHIVES / filename
        if not target.exists():
            request = urllib.request.Request(
                raw_base + urllib.parse.quote(filename),
                headers={"User-Agent": "ASSET_SIMU-asset-preparer/1.0"},
            )
            try:
                with urllib.request.urlopen(request, timeout=90) as response, target.open("wb") as output:
                    shutil.copyfileobj(response, output)
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                target.unlink(missing_ok=True)
                print(f"ERROR download {filename}: {exc}")
                failures += 1
                continue

        digest = sha256(target)
        if digest in seen_hashes:
            print(f"DUPLICATE {filename} == {seen_hashes[digest]} (sha256 {digest})")
            target.unlink()
            continue
        seen_hashes[digest] = filename
        print(f"OK {filename} sha256={digest}")

        if filename.lower().endswith(".zip"):
            destination = EXTRACTED / filename.removesuffix(".zip")
            try:
                safe_extract(target, destination)
            except (zipfile.BadZipFile, OSError, ValueError) as exc:
                print(f"ERROR extract {filename}: {exc}")
                failures += 1

    print(f"\nStaged sources in: {ARCHIVES}")
    print(f"Extracted ZIP contents in: {EXTRACTED}")
    print("Inspect and validate extracted files before moving any into public/assets/.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
