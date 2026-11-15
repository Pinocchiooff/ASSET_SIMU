# Sources d’assets proposées

## Pack CC0 Poly Haven

Le script [`scripts/fetch_polyhaven_pack.py`](../scripts/fetch_polyhaven_pack.py) récupère via l’API officielle de Poly Haven une sélection de textures PBR de terrain, un modèle de rocher et un HDRI. Les ressources sont annoncées CC0 par Poly Haven. Le script les place dans `source-assets/polyhaven/` et génère un rapport avec URLs et chemins d’API.

L’exécution n’a pas lieu sur GitHub par la simple présence du script : lancez-le depuis un clone local du dépôt avec Python 3 et un accès réseau :

```bash
python3 scripts/fetch_polyhaven_pack.py
```

Les assets téléchargés ne sont pas automatiquement publiés dans `public/assets/`. Vérifiez les fichiers et leurs tailles, optimisez les images, convertissez si nécessaire et ne complétez le manifeste runtime qu’avec les ressources effectivement préparées.

## Licence et attribution

Les fichiers Poly Haven sont proposés sous CC0 1.0, mais conservez les pages sources et vérifiez les informations de chaque asset. Pour toute autre source publique, vérifiez la licence de l’asset lui-même : une licence de dépôt ou la visibilité publique ne donne pas automatiquement le droit de réutiliser les fichiers.
