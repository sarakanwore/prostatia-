from app.registry.schemas import (
    MethodFiche,
    MethodParameter,
    MethodOutput,
)

pca_method = MethodFiche(
    id="pca",
    name="Analyse en Composantes Principales (ACP)",
    category="multivariate",
    description="Réduit la dimensionnalité d'un jeu de données de variables quantitatives tout en conservant le maximum d'information (inertie). Permet de visualiser les corrélations entre variables et les similarités entre individus.",
    inputs={
        "data": MethodParameter(
            type="array<array<float>>", 
            description="Tableau 2D (matrice) des variables quantitatives actives. Chaque colonne est une variable, chaque ligne un individu."
        ),
    },
    assumptions=[
        # En pratique, l'ACP est descriptive et n'a pas d'hypothèses probabilistes strictes.
        # Toutefois, elle nécessite des variables continues. Nous l'admettons par construction.
    ],
    fallback_if_assumptions_fail=[],
    outputs={
        "eigenvalues": MethodOutput(type="array<float>", description="Valeurs propres (Inertie) de chaque axe factoriel"),
        "explained_variance_ratio": MethodOutput(type="array<float>", description="Pourcentage de variance expliquée par chaque axe (en %)"),
        "variable_correlations": MethodOutput(type="array<array<float>>", description="Corrélations des variables avec les axes principaux (Cercle des corrélations)"),
        "individual_coordinates": MethodOutput(type="array<array<float>>", description="Coordonnées des individus sur les premiers axes factoriels")
    },
    numerical_method="sklearn.decomposition.PCA",
    limitations=[
        "Sensible aux valeurs aberrantes (outliers)",
        "N'analyse que les relations linéaires",
        "Ne gère que des variables quantitatives"
    ],
    references=[
        "Hotelling, H. (1933). Analysis of a complex of statistical variables into principal components."
    ]
)

MULTIVARIATE_METHODS = {
    pca_method.id: pca_method
}
