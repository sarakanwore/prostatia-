from app.registry.schemas import MethodFiche, MethodParameter, MethodOutput

def _common_inputs():
    return {
        "X": MethodParameter(type="array<float>", description="Data matrix (samples × features)"),
    }

PCA_FICHE = MethodFiche(
    id="pca",
    name="Analyse en composantes principales",
    category="multivariate_extended",
    description="Réduction linéaire de dimension en maximisant la variance.",
    inputs={**_common_inputs(), "n_components": MethodParameter(type="int", description="Nombre de composantes à retenir")},
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "components": MethodOutput(type="array<float>", description="Composantes principales (samples × n_components)"),
        "explained_variance": MethodOutput(type="array<float>", description="Variance expliquée par chaque composante"),
        "explained_variance_ratio": MethodOutput(type="array<float>", description="Ratio de variance expliquée"),
    },
    numerical_method="multivariate_extended.pca",
    limitations=["Suppose que les variables sont linéairement liées et centrées"],
    references=["Jolliffe, I.T. Principal Component Analysis (2002)"]
)

ICA_FICHE = MethodFiche(
    id="ica",
    name="Analyse en composantes indépendantes",
    category="multivariate_extended",
    description="Décomposition de signaux en composantes statistiquement indépendantes.",
    inputs={**_common_inputs(), "n_components": MethodParameter(type="int", description="Nombre de composantes à extraire"), "max_iter": MethodParameter(type="int", description="Itérations maximales")},
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "sources": MethodOutput(type="array<float>", description="Sources séparées (samples × n_components)"),
        "mixing_matrix": MethodOutput(type="array<float>", description="Matrice de mélange"),
        "unmixing_matrix": MethodOutput(type="array<float>", description="Matrice de démélange"),
    },
    numerical_method="multivariate_extended.ica",
    limitations=["Les sources doivent être non‑Gaussiennes"],
    references=["Hyvarinen, A., Oja, E. Independent Component Analysis (2000)"]
)

LDA_FICHE = MethodFiche(
    id="lda",
    name="Analyse discriminante linéaire",
    category="multivariate_extended",
    description="Projection qui maximise la séparabilité entre classes.",
    inputs={**_common_inputs(), "y": MethodParameter(type="array<int>", description="Étiquettes de classe"), "n_components": MethodParameter(type="int", description="Nombre de composantes à retenir (max = n_classes‑1)")},
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "components": MethodOutput(type="array<float>", description="Projection des données (samples × n_components)"),
        "explained_variance_ratio": MethodOutput(type="array<float>", description="Ratio de variance expliquée par chaque axe"),
    },
    numerical_method="multivariate_extended.lda",
    limitations=["Suppose la normalité des classes et covariances égales"],
    references=["Fisher, R.A. The Use of Multiple Measurements in Taxonomic Problems (1936)"]
)

TSNE_FICHE = MethodFiche(
    id="tsne",
    name="t‑Distributed Stochastic Neighbor Embedding",
    category="multivariate_extended",
    description="Projection non‑linéaire pour visualisation en 2‑3 dimensions.",
    inputs={**_common_inputs(), "n_components": MethodParameter(type="int", description="Dimension de la visualisation (2 ou 3)"), "perplexity": MethodParameter(type="float", description="Paramètre perplexité"), "learning_rate": MethodParameter(type="float", description="Taux d’apprentissage")},
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={"embedding": MethodOutput(type="array<float>", description="Coordonnées projetées (samples × n_components)")},
    numerical_method="multivariate_extended.tsne",
    limitations=["Non déterministe, sensible aux paramètres"],
    references=["van der Maaten, L., Hinton, G. Visualizing Data using t‑SNE (2008)"]
)

UMAP_FICHE = MethodFiche(
    id="umap",
    name="Uniform Manifold Approximation and Projection",
    category="multivariate_extended",
    description="Algorithme de réduction de dimension basé sur la théorie des graphes de voisinage.",
    inputs={**_common_inputs(), "n_components": MethodParameter(type="int", description="Dimension de l’embedding"), "n_neighbors": MethodParameter(type="int", description="Taille du voisinage"), "min_dist": MethodParameter(type="float", description="Distance minimale entre points dans l’espace projeté")},
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={"embedding": MethodOutput(type="array<float>", description="Embeddage (samples × n_components)")},
    numerical_method="multivariate_extended.umap_embed",
    limitations=["Sensibilité aux hyper‑paramètres"],
    references=["McInnes, L., Healy, J., Melville, J. UMAP: Uniform Manifold Approximation and Projection (2018)"]
)

DBSCAN_FICHE = MethodFiche(
    id="dbscan",
    name="Density‑Based Spatial Clustering of Applications with Noise",
    category="multivariate_extended",
    description="Algorithme de clustering qui identifie des régions de haute densité.",
    inputs={**_common_inputs(), "eps": MethodParameter(type="float", description="Rayon du voisinage"), "min_samples": MethodParameter(type="int", description="Nombre minimal de points pour former un cluster")},
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={"labels": MethodOutput(type="array<int>", description="Label de cluster pour chaque point (-1 = bruit)"), "core_sample_indices": MethodOutput(type="array<int>", description="Indices des points noyau")},
    numerical_method="multivariate_extended.dbscan",
    limitations=["Dépend fortement du choix de eps"],
    references=["Ester, M., Kriegel, H.-P., Sander, J., Xu, X. A Density‑based Algorithm for Discovering Clusters (1996)"]
)

MULTIVARIATE_EXTENDED_METHODS = {
    PCA_FICHE.id: PCA_FICHE,
    ICA_FICHE.id: ICA_FICHE,
    LDA_FICHE.id: LDA_FICHE,
    TSNE_FICHE.id: TSNE_FICHE,
    UMAP_FICHE.id: UMAP_FICHE,
    DBSCAN_FICHE.id: DBSCAN_FICHE,
}
