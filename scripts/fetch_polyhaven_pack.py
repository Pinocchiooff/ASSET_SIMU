#!/usr/bin/env python3
"""Download a small, curated CC0 starter pack from Poly Haven's public API.

Downloads are staged under source-assets/polyhaven/. They are not added to the
runtime manifest automatically: inspect model formats, file sizes and credits
before promoting files to public/assets/.
"""
from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "source-assets" / "polyhaven"
API = "https://api.polyhaven.com"
USER_AGENT = "ASSET_SIMU-PolyHaven-Downloader/1.0 (asset staging)"

# Poly Haven assets are CC0. Check the asset page and API response before use.
PACK = {
    "textures": {
        "aerial_grass_rock": ["diffuse", "nor_gl", "roughness", "ao"],
        "asphalt_02": ["diffuse", "nor_gl", "roughness", "ao"],
        "brown_mud_02": ["diffuse", "nor_gl", "roughness", "ao"],
        "forest_ground_04": ["diffuse", "nor_gl", "roughness", "ao"],
        "coast_sand_rocks_02": ["diffuse", "nor_gl", "roughness", "ao"],
    },
    "models": {
        "rock_boulder_dry": ["model"],
    },
    "hdris": {
        "autumn_field_puresky": ["hdri"],
    },
}


def get_json(url: str) -> Any:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def url_records(node: Any, path: tuple[str, ...] = ()):
    if isinstance(node, dict):
        direct = node.get("url")
        if isinstance(direct, str) and direct.startswith(("https://", "http://")):
            yield path, direct
        for key, value in node.items():
            if key != "url":
                yield from url_records(value, path + (str(key),))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from url_records(value, path + (str(index),))


def score_record(path: tuple[str, ...], url: str, kind: str, map_name: str | None = None):
    text = " ".join(path + (url,)).lower()
    if kind == "model":
        if not any(ext in text for ext in (".glb", ".gltf", ".zip")):
            return -1
        score = 30 if ".glb" in text else (20 if ".gltf" in text else 10)
    elif kind == "hdri":
        if not any(ext in text for ext in (".exr", ".hdr")):
            return -1
        score = 20
    else:
        aliases = {
            "diffuse": ("diffuse", "albedo", "color", "colour"),
            "nor_gl": ("nor_gl", "normal_gl", "normal"),
            "roughness": ("roughness", "rough"),
            "ao": ("ao", "ambientocclusion", "ambient_occlusion"),
        }
        if not any(alias in text for alias in aliases.get(map_name or "", ())):
            return -1
        if not any(ext in text for ext in (".jpg", ".jpeg", ".png", ".exr", ".zip")):
            return -1
        score = 20
    # Prefer web-sized files, then use 2k as fallback.
    if "1k" in text or "1024" in text:
        score += 12
    elif "2k" in text or "2048" in text:
        score += 8
    elif "4k" in text or "4096" in text:
        score += 2
    return score


def safe_name(url: str, fallback: str) -> str:
    name = Path(urllib.parse.urlparse(url).path).name
    name = urllib.parse.unquote(name)
    if not name or name in (".", ".."):
        name = fallback
    return re.sub(r"[^A-Za-z0-9._-]", "_", name)


def download(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=180) as response, target.open("wb") as out:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    report = {"source": "Poly Haven", "license": "CC0 1.0", "assets": []}
    errors = []

    for category, assets in PACK.items():
        for slug, maps in assets.items():
            try:
                records = list(url_records(get_json(f"{API}/files/{urllib.parse.quote(slug)}")))
                if not records:
                    raise RuntimeError("API returned no downloadable URLs")
                selected = []
                if maps == ["model"]:
                    candidates = [(score_record(p, u, "model"), p, u) for p, u in records]
                    candidates = [item for item in candidates if item[0] >= 0]
                    if candidates:
                        selected.append(("model", max(candidates, key=lambda x: x[0])))
                elif maps == ["hdri"]:
                    candidates = [(score_record(p, u, "hdri"), p, u) for p, u in records]
                    candidates = [item for item in candidates if item[0] >= 0]
                    if candidates:
                        selected.append(("hdri", max(candidates, key=lambda x: x[0])))
                else:
                    for map_name in maps:
                        candidates = [(score_record(p, u, "texture", map_name), p, u) for p, u in records]
                        candidates = [item for item in candidates if item[0] >= 0]
                        if candidates:
                            selected.append((map_name, max(candidates, key=lambda x: x[0])))

                if not selected:
                    raise RuntimeError("No matching web/model files found in API response")
                for map_name, (_, path, url) in selected:
                    filename = safe_name(url, f"{slug}_{map_name}")
                    target = DEST / category / slug / filename
                    if not target.exists():
                        download(url, target)
                    report["assets"].append({
                        "id": slug,
                        "category": category,
                        "map": map_name,
                        "file": target.relative_to(ROOT).as_posix(),
                        "source_url": f"https://polyhaven.com/a/{slug}",
                        "download_url": url,
                        "license": "CC0 1.0",
                        "api_path": list(path),
                    })
                    print(f"OK {slug} {map_name}: {target.relative_to(ROOT)}")
            except (urllib.error.URLError, TimeoutError, OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
                errors.append(f"{slug}: {exc}")
                print(f"SKIP {slug}: {exc}", file=sys.stderr)

    (DEST / "download-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"\nStaged files: {DEST}")
    print("Inspect each file and its report before promoting it into public/assets/.")
    if errors:
        print("Some assets could not be resolved automatically:", file=sys.stderr)
        print("\n".join(errors), file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
