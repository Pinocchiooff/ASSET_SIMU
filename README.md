# ASSET_SIMU

Dépôt public pour stocker, préparer et documenter des assets 3D de simulateur drone pour Google AI Studio.

## Ce que contient le dépôt

- `public/assets/` : ressources prêtes à charger dans le runtime web (`GLB`, `PNG`, `HDR`, fiches de matériau).
- `source-assets/` : archives, pack sources et scripts de récupération à partir de sources publiques autorisées.
- `docs/` : documentation d’usage, inventaire des assets et consignes AI Studio.
- `scripts/` : scripts de récupération et validation des assets.

## Structure recommandée

```text
ASSET_SIMU/
├── README.md
├── docs/
│   ├── AI_STUDIO_SETUP.md
│   ├── ASSET_INVENTORY.md
│   └── EXTERNAL_ASSET_SOURCES.md
├── public/
│   └── assets/
│       ├── manifest.json
│       ├── environments/
│       ├── models/
│       └── textures/
├── scripts/
│   ├── fetch_assets.py
│   └── fetch_polyhaven_pack.py
└── source-assets/
    ├── polyhaven/
    └── README.md
```

## Pack de départ recommandé

Le pack de départ est basé sur des sources ouvertes et largement utilisées, dont les licences sont compatibles avec une utilisation de simulation et de rendu web :

- Poly Haven : CC0 pour la majorité des assets, y compris modèles glTF/GLB, textures PBR et HDRI.
- ambientCG : textures PBR CC0, très utiles pour les surfaces et terrains.
- Quaternius, 3DAssets.dev : modèles 3D CC0 ou permissifs pour végétation et props, à valider par asset.

## Typologie d’assets à privilégier

1. Terrain / surface
   - grass_rock
   - forest_ground
   - mud
   - asphalt
   - concrete
   - sand / coast rocks

2. Modèles 3D
   - rocher / pierre
   - arbre / palmier / buisson
   - bâtiments / hangars / tours
   - drone / quadricoptère / avion léger

3. Environnement
   - HDRI de ciel / paysage
   - lumière d’ambiance pour rendu réaliste

## AI Studio

Le dépôt est prêt à être utilisé dans un projet AI Studio qui charge des fichiers statiques depuis le dossier `public/`.

- Les modèles GLB doivent être chargés en `GLTFLoader`.
- Les textures PBR doivent être associées aux matériaux via `map`, `normalMap`, `roughnessMap`, etc.
- Les HDRI doivent être chargés via `RGBELoader` ou via le pipeline de rendu du projet.

Voir aussi : `docs/AI_STUDIO_SETUP.md`.

## Règle de validation avant usage

Avant qu’un asset soit ajouté à `public/assets/`, vérifier :

- format supporté (`.glb`, `.png`, `.jpg`, `.hdr`, `.exr`)
- licence compatible
- taille du fichier acceptable pour le web
- présence des maps nécessaires (albedo, normal, roughness, AO)
- cohérence de la nomenclature

## Sources officielles de référence

- Poly Haven API : https://api.polyhaven.com
- Poly Haven GitHub : https://github.com/Poly-Haven/Public-API
- ambientCG : https://ambientcg.com
- Quaternius : https://quaternius.com
- 3DAssets.dev : https://www.3dassets.dev

## À noter

Le dépôt ne doit pas contenir d’assets non vérifiés, ni des fichiers sans licence claire. Les scripts fournis permettent de préparer les sources, mais l’intégration finale dans `public/assets/` doit toujours rester manuelle et validée.
