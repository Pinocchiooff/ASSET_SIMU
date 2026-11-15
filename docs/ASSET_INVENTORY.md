# Inventaire des assets

## Provenance

Assets utilisateur actuellement répertoriés dans le dépôt public [`Pinocchiooff/aeroesiee-ai-studio`](https://github.com/Pinocchiooff/aeroesiee-ai-studio). Le contenu des archives ZIP n’a pas été inspecté dans cet environnement ; l’inventaire ci-dessous est basé sur les noms et extensions visibles. La licence doit être confirmée sur la page source de chaque asset avant réutilisation.

| Fichier source | Type visible | Traitement cible |
|---|---|---|
| `aerial_asphalt_01_1k.gltf.zip` | archive glTF | Extraire les textures, identifier les cartes PBR, ranger sous `textures/asphalt/` |
| `aerial_grass_rock_1k.gltf.zip` | archive glTF | Extraire les cartes PBR sous `textures/ground/grass_rock/` |
| `aerial_rocks_04_2k.gltf.zip` | archive glTF | Extraire les cartes PBR sous `textures/ground/rocks/` |
| `asphalt_02_2k.gltf.zip` | archive glTF | Extraire les cartes PBR sous `textures/asphalt/` |
| `autumn_field_puresky_4k.hdr` | environnement HDR | Placer sous `environments/`; charger avec RGBELoader et vérifier son poids/résolution |
| `bark_willow_1k.gltf.zip` | archive glTF | Extraire et inspecter ; source de matériau/asset à confirmer |
| `brown_mud_02_1k.gltf.zip` | archive glTF | Extraire les cartes PBR sous `textures/ground/mud/` |
| `brown_mud_leaves_01_2k.gltf.zip` | archive glTF | Extraire les cartes PBR sous `textures/ground/mud_leaves/` |
| `brushed_concrete_04_1k.gltf.zip` | archive glTF | Extraire les cartes PBR sous `textures/concrete/` |
| `coast_rocks_02_diff_1k.jpg` | albedo JPG | Carte couleur sous `textures/coast_rocks/` |
| `coast_rocks_02_nor_gl_1k.exr` | normal EXR | Convertir en PNG/WebP compatible avant usage courant dans Three.js |
| `coast_rocks_02_rough_1k.exr` | roughness EXR | Convertir en PNG/WebP compatible avant usage courant dans Three.js |
| `coast_sand_04_1k.gltf.zip` | archive glTF | Extraire les cartes PBR sous `textures/ground/sand/` |
| `coast_sand_rocks_02_2k.gltf.zip` | archive glTF | Extraire les cartes PBR sous `textures/coast_rocks/` |
| `concrete_road_barrier_2k.blend.zip` | archive Blender | Source non chargeable directement ; examiner et exporter modèle en GLB si utile |
| `corrugated_iron_02_1k.gltf.zip` | archive glTF | Extraire les cartes PBR sous `textures/metal/` |
| `covered_car_2k.blend.zip` | archive Blender | Source non chargeable directement ; examiner et exporter en GLB si utile |
| `exterior_aircon_unit_01_diff_2k.png` | texture PNG | Texture d’objet ; associer au modèle correspondant après identification |
| `exterior_aircon_unit_01_metal_2k.png` | texture PNG | Carte métallique ; vérifier la sémantique du canal/source |
| `exterior_aircon_unit_01_nor_gl_2k.png` | texture PNG | Carte normale OpenGL |
| `exterior_aircon_unit_01_opacity_2k.png` | texture PNG | Carte d’opacité si le matériau la requiert |
| `exterior_aircon_unit_01_rough_2k.png` | texture PNG | Carte de rugosité |
| `exterior_aircon_unit_02_diff_2k.png` | texture PNG | Texture d’objet ; associer au modèle correspondant après identification |
| `exterior_aircon_unit_02_metal_2k.png` | texture PNG | Carte métallique ; vérifier la sémantique du canal/source |
| `exterior_aircon_unit_02_nor_gl_2k.png` | texture PNG | Carte normale OpenGL |
| `exterior_aircon_unit_02_rough_2k.png` | texture PNG | Carte de rugosité |
| `exterior_aircon_unit_2k.blend` | projet Blender | Source non chargeable directement ; exporter en GLB si utile |
| `exterior_aircon_unit_rusted_01_diff_2k.png` | texture PNG | Texture d’objet rouillé ; associer au bon modèle |
| `exterior_aircon_unit_rusted_01_metal_2k.png` | texture PNG | Carte métallique ; vérifier les données/canaux |
| `exterior_aircon_unit_rusted_01_nor_gl_2k.png` | texture PNG | Carte normale OpenGL |
| `exterior_aircon_unit_rusted_01_rough_2k.png` | texture PNG | Carte de rugosité |
| `exterior_aircon_unit_rusted_02_diff_2k.png` | texture PNG | Texture d’objet rouillé ; associer au bon modèle |
| `exterior_aircon_unit_rusted_02_metal_2k.png` | texture PNG | Carte métallique ; vérifier les données/canaux |
| `venice_sunset_4k.hdr` | environnement HDR | Placer sous `environments/`; vérifier son poids/résolution |
| `weathered_plank_siding_1k.gltf.zip` | archive glTF | Extraire les cartes PBR sous `textures/wood/` |
| `wood_inlaid_stone_wall_1k.gltf.zip` | archive glTF | Extraire les cartes PBR ; matériau mixte bois/pierre à examiner |

## Doublons

Aucun doublon binaire exact ne peut être confirmé à partir des seuls noms. Le script de préparation calcule les empreintes SHA-256 des fichiers téléchargés et évite de réenregistrer les ZIP identiques. Les textures peuvent être sémantiquement redondantes sans être identiques ; faites une comparaison visuelle avant d’en supprimer.

## Priorités simulateur drone

1. Sol : `aerial_grass_rock`, `brown_mud_02`, `brown_mud_leaves_01`.
2. Pistes/aires : `aerial_asphalt_01`, `asphalt_02`, `brushed_concrete_04`.
3. Rivage/roches : assets `coast_*` et `aerial_rocks_04`.
4. Éclairage : choisir un seul HDRI de départ, puis réduire sa résolution pour le web si nécessaire.
5. Objets : les fichiers Blender et les archives doivent être convertis/validés en GLB avant intégration runtime.

## Licence

Compléter `public/assets/manifest.json` avec l’auteur, la licence vérifiée et l’URL précise de chaque asset. Ne pas inscrire CC0 par défaut sans vérification de la fiche de téléchargement correspondante.
