"""
Référentiel natif des limites administratives GeoJSON WGS84 (EPSG:4326)
pour le Togo et l'espace UEMOA (Cahier des charges STATIA §7.4).
"""

from typing import Dict, Any

TOGO_REGIONS: Dict[str, Any] = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": "TGO-SAV",
            "properties": {
                "name": "Savanes",
                "code": "SAV",
                "capital": "Dapaong",
                "country": "Togo"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-0.05, 10.10],
                    [0.85, 10.10],
                    [0.85, 11.15],
                    [-0.05, 11.15],
                    [-0.05, 10.10]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "TGO-KAR",
            "properties": {
                "name": "Kara",
                "code": "KAR",
                "capital": "Kara",
                "country": "Togo"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [0.30, 9.30],
                    [1.40, 9.30],
                    [1.40, 10.10],
                    [0.30, 10.10],
                    [0.30, 9.30]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "TGO-CEN",
            "properties": {
                "name": "Centrale",
                "code": "CEN",
                "capital": "Sokodé",
                "country": "Togo"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [0.40, 8.30],
                    [1.60, 8.30],
                    [1.60, 9.30],
                    [0.40, 9.30],
                    [0.40, 8.30]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "TGO-PLA",
            "properties": {
                "name": "Plateaux",
                "code": "PLA",
                "capital": "Atakpamé",
                "country": "Togo"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [0.55, 6.80],
                    [1.70, 6.80],
                    [1.70, 8.30],
                    [0.55, 8.30],
                    [0.55, 6.80]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "TGO-MAR",
            "properties": {
                "name": "Maritime",
                "code": "MAR",
                "capital": "Lomé",
                "country": "Togo"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [1.00, 6.05],
                    [1.85, 6.05],
                    [1.85, 6.80],
                    [1.00, 6.80],
                    [1.00, 6.05]
                ]]
            }
        }
    ]
}

UEMOA_COUNTRIES: Dict[str, Any] = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": "BEN",
            "properties": {"name": "Bénin", "code": "BEN", "capital": "Porto-Novo", "currency": "XOF"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[1.6, 6.2], [3.8, 6.2], [3.8, 12.4], [1.6, 12.4], [1.6, 6.2]]]
            }
        },
        {
            "type": "Feature",
            "id": "BFA",
            "properties": {"name": "Burkina Faso", "code": "BFA", "capital": "Ouagadougou", "currency": "XOF"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[-5.5, 9.4], [2.4, 9.4], [2.4, 15.1], [-5.5, 15.1], [-5.5, 9.4]]]
            }
        },
        {
            "type": "Feature",
            "id": "CIV",
            "properties": {"name": "Côte d'Ivoire", "code": "CIV", "capital": "Yamoussoukro", "currency": "XOF"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[-8.6, 4.3], [-2.5, 4.3], [-2.5, 10.7], [-8.6, 10.7], [-8.6, 4.3]]]
            }
        },
        {
            "type": "Feature",
            "id": "GNB",
            "properties": {"name": "Guinée-Bissau", "code": "GNB", "capital": "Bissau", "currency": "XOF"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[-16.7, 10.9], [-13.6, 10.9], [-13.6, 12.7], [-16.7, 12.7], [-16.7, 10.9]]]
            }
        },
        {
            "type": "Feature",
            "id": "MLI",
            "properties": {"name": "Mali", "code": "MLI", "capital": "Bamako", "currency": "XOF"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[-12.2, 10.1], [4.3, 10.1], [4.3, 25.0], [-12.2, 25.0], [-12.2, 10.1]]]
            }
        },
        {
            "type": "Feature",
            "id": "NER",
            "properties": {"name": "Niger", "code": "NER", "capital": "Niamey", "currency": "XOF"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[0.2, 11.7], [16.0, 11.7], [16.0, 23.5], [0.2, 23.5], [0.2, 11.7]]]
            }
        },
        {
            "type": "Feature",
            "id": "SEN",
            "properties": {"name": "Sénégal", "code": "SEN", "capital": "Dakar", "currency": "XOF"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[-17.5, 12.3], [-11.3, 12.3], [-11.3, 16.7], [-17.5, 16.7], [-17.5, 12.3]]]
            }
        },
        {
            "type": "Feature",
            "id": "TGO",
            "properties": {"name": "Togo", "code": "TGO", "capital": "Lomé", "currency": "XOF"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[-0.05, 6.05], [1.85, 6.05], [1.85, 11.15], [-0.05, 11.15], [-0.05, 6.05]]]
            }
        }
    ]
}

def get_boundaries(zone: str) -> Dict[str, Any]:
    zone_upper = zone.upper()
    if zone_upper in ("TGO", "TOGO"):
        return TOGO_REGIONS
    elif zone_upper in ("UEMOA", "WAEMU"):
        return UEMOA_COUNTRIES
    else:
        raise ValueError(f"Zone géographique non supportée: '{zone}'. Utilisez 'TGO' ou 'UEMOA'.")
