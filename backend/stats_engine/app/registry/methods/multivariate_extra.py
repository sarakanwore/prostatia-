from app.registry.schemas import MethodFiche, MethodParameter, MethodAssumption, MethodOutput

# Analyse Factorielle des Correspondances (AFC) – deux variables qualitatives
afc_method = MethodFiche(
    id="afc",
    name="Analyse Factorielle des Correspondances (AFC)",
    category="multivariate_extra",
    description="Analyse les relations entre deux variables qualitatives via la décomposition en valeurs singulières des fréquences standardisées.",
    inputs={
        "contingency_table": MethodParameter(type="array<array<int>>", description="Tableau de contingence (effectifs)."),
    },
    assumptions=[
        MethodAssumption(
            id="sufficient_counts",
            name="Effectifs suffisants",
            test_method="contingency_expected_freq",
            description="Toutes les effectifs attendus doivent être > 5 pour garantir la validité de l'AFC."
        ),
    ],
    fallback_if_assumptions_fail=[],
    outputs={
        "row_coordinates": MethodOutput(type="array<array<float>>", description="Coordonnées des lignes du tableau dans l'espace factoriel."),
        "col_coordinates": MethodOutput(type="array<array<float>>", description="Coordonnées des colonnes du tableau dans l'espace factoriel."),
        "explained_inertia": MethodOutput(type="array<float>", description="Inertie (variance) expliquée par chaque facteur."),
    },
    numerical_method="scipy.wrapper.execute_afc",
    limitations=["Suppose que les effectifs sont suffisamment grands.", "Ne gère que deux variables qualitatives (tableau de contingence 2D)."],
    references=["Greenacre, M. (2017). Correspondence Analysis in Practice."]
)

# Analyse des Correspondances Multiples (ACM) – plusieurs variables qualitatives
acm_method = MethodFiche(
    id="acm",
    name="Analyse des Correspondances Multiples (ACM)",
    category="multivariate_extra",
    description="Extension de l'AFC à plus de deux variables qualitatives via la concaténation des indicatrices.",
    inputs={
        "indicator_matrix": MethodParameter(type="array<array<int>>", description="Matrice indicatrice (dummy) des variables qualitatives."),
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "coordinates": MethodOutput(type="array<array<float>>", description="Coordonnées des modalités dans l'espace factoriel."),
        "explained_inertia": MethodOutput(type="array<float>", description="Inertie expliquée par chaque facteur."),
    },
    numerical_method="scipy.wrapper.execute_acm",
    limitations=["Peut être coûteux en mémoire pour un grand nombre de modalités."],
    references=["Le Roux, B., & Rouanet, H. (2004). Correspondence Analysis Results Interpretation."]
)

# Classification Ascendante Hiérarchique (CAH)
cah_method = MethodFiche(
    id="cah",
    name="Classification Ascendante Hiérarchique (CAH)",
    category="multivariate_extra",
    description="Regroupe les individus en clusters hiérarchiques via agglomération.",
    inputs={
        "data": MethodParameter(type="array<array<float>>", description="Matrice de données (observations × variables)."),
        "n_clusters": MethodParameter(type="int", description="Nombre de clusters souhaités (cut du dendrogramme)."),
        "linkage": MethodParameter(type="string", description="Méthode de liaison : 'ward', 'complete', 'average', 'single'."),
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "labels": MethodOutput(type="array<int>", description="Étiquette de cluster attribuée à chaque observation."),
        "linkage_matrix": MethodOutput(type="array<array<float>>", description="Matrice de liaison (format scipy.cluster.hierarchy)."),
    },
    numerical_method="scipy.wrapper.execute_cah",
    limitations=["Complexité O(n^2) en temps et mémoire."],
    references=["Murtagh, F., & Legendre, P. (2014). Ward's hierarchical agglomerative clustering method."]
)

# K‑Means clustering
kmeans_method = MethodFiche(
    id="kmeans",
    name="K‑Means Clustering",
    category="multivariate_extra",
    description="Partitionne les observations en k groupes en minimisant la variance intra‑cluster.",
    inputs={
        "data": MethodParameter(type="array<array<float>>", description="Matrice de données (observations × variables)."),
        "n_clusters": MethodParameter(type="int", description="Nombre de clusters k."),
        "max_iter": MethodParameter(type="int", description="Nombre maximal d'itérations."),
        "init": MethodParameter(type="string", description="Méthode d'initialisation, ex. 'k-means++' ou 'random'."),
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "centers": MethodOutput(type="array<array<float>>", description="Coordonnées des centres de chaque cluster."),
        "labels": MethodOutput(type="array<int>", description="Étiquette du cluster pour chaque observation."),
        "inertia": MethodOutput(type="float", description="Somme des distances au carré des points aux centres de leurs clusters."),
    },
    numerical_method="scipy.wrapper.execute_kmeans",
    limitations=["Suppose que les clusters sont de forme sphérique et de taille similaire."],
    references=["MacQueen, J. (1967). Some methods for classification and analysis of multivariate observations."]
)

# Export dictionary for registration
MULTIVARIATE_EXTRA_METHODS = {
    afc_method.id: afc_method,
    acm_method.id: acm_method,
    cah_method.id: cah_method,
    kmeans_method.id: kmeans_method,
}
