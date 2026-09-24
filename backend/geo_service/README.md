# STATIA Geospatial & Cartography Service (geo_service)

Version 1.0.0

Le **geo_service** est le microservice de cartographie et d'analyse territoriale de la plateforme **STATIA** (Cahier des charges, Sections 3.5, 4.2 et 7.4).

## Fonctionnalités
- **Fonds de cartes natifs** :
  - **Togo (5 Régions)** : Savanes, Kara, Centrale, Plateaux, Maritime (incluant Grand Lomé).
  - **Espace UEMOA (8 pays)** : Bénin, Burkina Faso, Côte d'Ivoire, Guinée-Bissau, Mali, Niger, Sénégal, Togo.
- **Cartes choroplèthes** : Jointure des séries statistiques avec les polygones et génération de styles thématiques (breaks, quantiles, échelles de couleurs).
- **Rattachement spatial (Point-in-Polygon)** : Localisation de points GPS dans leur région administrative d'appartenance.
- **Cartes de densité** : Calcul de grille spatiale 2D.

## Démarrage local
```bash
poetry install
poetry run uvicorn app.main:app --port 8004 --reload
```
