# Préparation et intégration dans AI Studio

## État et workflow

Le dépôt stocke les sources dans `source-assets/` et les fichiers prêts au runtime sous `public/assets/`. Les archives et fichiers Blender ne sont pas des assets runtime directement chargeables. Après exécution du script de récupération, inspectez les contenus extraits, puis copiez les cartes ou modèles validés dans les dossiers runtime et complétez le manifeste.

### Récupérer les archives sources

Depuis un clone local de ce dépôt, utilisez Python 3 :

```bash
python3 scripts/fetch_assets.py
```

Le script télécharge uniquement les fichiers listés du dépôt source public, vérifie SHA-256, protège contre les chemins ZIP dangereux et garde les archives dans `source-assets/archives/`. Il place les fichiers extraits dans `source-assets/extracted/<nom-asset>/` pour inspection ; il ne prétend pas convertir automatiquement les `.blend`, EXR ou matériaux glTF en assets web optimisés.

### Préparer les fichiers runtime

- GLB : valider dans un visualiseur glTF et placer dans `public/assets/models/...`; prévoir GLTFLoader.
- Textures : identifier les images correspondant à `diffuse/albedo`, `normal`, `roughness`, `metalness`, `opacity`, etc. Ne renommez pas les fichiers tant que leur association n’est pas comprise.
- EXR : convertir les cartes de données en PNG/WebP 8 bits ou autre format supporté, en préservant les canaux et sans appliquer de correction gamma aux données.
- HDRI : garder un fichier raisonnable en taille et charger avec RGBELoader/PMREMGenerator dans Three.js.
- Blender : exporter en GLB seulement après vérification des matériaux, textures, unités, axes et nœuds mobiles.
- Manifeste : référencer uniquement des fichiers runtime réellement présents. Les chemins sont relatifs à `public/assets/`.

## Prompt à copier dans AI Studio

> Utilise `docs/ASSET_INVENTORY.md`, `docs/AI_STUDIO_SETUP.md` et `public/assets/manifest.json` comme source de vérité. Les fichiers dans `source-assets/` sont des sources à examiner, pas des ressources runtime prêtes. Ne tente pas de charger un ZIP ou un fichier Blender comme un modèle GLB. Ne référence que les fichiers réellement présents dans `public/assets/`. Implémente le chargement selon le moteur du projet (si Three.js : GLTFLoader pour GLB, TextureLoader pour les textures web compatibles, RGBELoader pour HDRI), avec gestion d’erreur et fallback. Respecte les licences et crédits du manifeste. Avant de coder, liste les fichiers runtime disponibles et les formats nécessitant conversion.
