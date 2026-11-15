# ASSET_SIMU — ressources 3D du simulateur de drone

Dépôt public destiné à centraliser les assets, leurs licences et leur manifeste d’intégration pour l’application web Google AI Studio.

## État actuel

Le dépôt ne contenait que le README du modèle AI Studio au début de la préparation. Les assets déjà téléversés se trouvent dans l’autre dépôt public [`Pinocchiooff/aeroesiee-ai-studio`](https://github.com/Pinocchiooff/aeroesiee-ai-studio), à sa racine. Les outils disponibles ici peuvent préparer les fichiers de catalogue et de traitement, mais ne peuvent pas recopier/décompresser ces binaires dans ce dépôt. **Les assets ne sont donc pas encore installés dans `ASSET_SIMU`.**

Consultez [`docs/ASSET_INVENTORY.md`](docs/ASSET_INVENTORY.md) pour l’inventaire connu, puis exécutez le script local de préparation après avoir cloné ce dépôt. Le script télécharge les fichiers connus depuis le dépôt source, vérifie les SHA-256, prévient les doublons identiques et extrait les ZIP de manière sûre.

## Organisation cible

```text
public/assets/
├── manifest.json
├── environments/             # HDRI pour l’éclairage/ciel
├── models/                   # GLB prêts à charger avec GLTFLoader
│   ├── buildings/
│   ├── props/
│   ├── vegetation/
│   └── vehicles/
└── textures/                 # cartes PBR, regroupées par matériau
    ├── asphalt/
    ├── concrete/
    ├── coast_rocks/
    ├── ground/
    ├── metal/
    └── wood/

source-assets/                 # archives et projets sources non directement chargeables
```

Les fichiers `.blend` et `.gltf.zip` ne sont pas directement chargeables par l’application comme un GLB prêt à l’emploi. Les archives glTF doivent être examinées et les cartes PBR extraites/repérées ; les fichiers Blender doivent être exportés en GLB. Le manifeste ne doit lister comme `ready` que les fichiers réellement présents et utilisables.

## AI Studio

Dans un projet web utilisant `public/`, les fichiers statiques sont généralement accessibles sous `/assets/...`. Utilisez `GLTFLoader` pour les `.glb`, `RGBELoader` pour les HDRI et des textures compatibles avec les chargeurs de Three.js pour les cartes PBR. Le manifeste n’effectue pas lui-même le chargement : le code de l’application doit l’interpréter. Consultez [`docs/AI_STUDIO_SETUP.md`](docs/AI_STUDIO_SETUP.md).

Vérifiez les licences asset par asset avant publication ou usage. Les fichiers issus d’un dépôt public ne sont pas automatiquement libres de droits. Gardez les crédits et les URL de source dans le manifeste.
