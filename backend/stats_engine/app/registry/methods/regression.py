from app.registry.schemas import (
    MethodFiche,
    MethodParameter,
    MethodAssumption,
    MethodOutput,
)

linear_regression = MethodFiche(
    id="linear_regression",
    name="Régression Linéaire Simple (OLS)",
    category="regression",
    description="Modélise la relation linéaire entre une variable dépendante continue et une ou plusieurs variables indépendantes.",
    inputs={
        "X": MethodParameter(type="array<float>", description="Variable(s) indépendante(s) ou explicative(s)"),
        "y": MethodParameter(type="array<float>", description="Variable dépendante ou cible"),
    },
    assumptions=[], # Pour simplifier dans cette v0, on n'ajoute pas de fallback complexe. On pourrait tester la normalité des résidus.
    fallback_if_assumptions_fail=[],
    outputs={
        "r_squared": MethodOutput(type="float", description="Coefficient de détermination (R²)"),
        "p_value": MethodOutput(type="float", description="P-value globale du modèle"),
        "slope": MethodOutput(type="float", description="Pente (coefficient de X)"),
        "intercept": MethodOutput(type="float", description="Ordonnée à l'origine (constante)")
    },
    numerical_method="scipy.stats.linregress",
    limitations=[
        "Ne modélise que des relations linéaires",
        "Très sensible aux valeurs aberrantes",
    ],
    references=[
        "Legendre (1805). Nouvelle méthode pour la détermination des orbites des comètes.",
    ],
)

multiple_linear_regression = MethodFiche(
    id="multiple_linear_regression",
    name="Régression Linéaire Multiple",
    category="regression",
    description="Modélise la relation linéaire entre une variable dépendante continue et plusieurs variables indépendantes.",
    inputs={
        "X": MethodParameter(type="array<array<float>>", description="Matrice des variables indépendantes (features)"),
        "y": MethodParameter(type="array<float>", description="Vecteur de la variable dépendante (cible)"),
    },
    assumptions=[
        MethodAssumption(
            id="no_multicollinearity",
            name="Absence de multicolinéarité",
            test_method="vif",
            description="Les variables indépendantes ne doivent pas être trop corrélées entre elles."
        )
    ],
    fallback_if_assumptions_fail=[],
    outputs={
        "r_squared": MethodOutput(type="float", description="Coefficient de détermination (R²)"),
        "adj_r_squared": MethodOutput(type="float", description="R² ajusté"),
        "f_statistic": MethodOutput(type="float", description="Statistique F du modèle global"),
        "p_value": MethodOutput(type="float", description="P-value globale du modèle"),
        "coefficients": MethodOutput(type="array<float>", description="Coefficients pour chaque variable de X"),
        "intercept": MethodOutput(type="float", description="Ordonnée à l'origine (constante)")
    },
    numerical_method="statsmodels.api.OLS",
    limitations=[
        "Suppose une relation linéaire additive",
        "Sensible aux valeurs aberrantes et à la multicolinéarité",
    ],
    references=[
        "Legendre (1805). Nouvelle méthode pour la détermination des orbites des comètes.",
    ],
)

REGRESSION_METHODS = {
    linear_regression.id: linear_regression,
    multiple_linear_regression.id: multiple_linear_regression,
}
