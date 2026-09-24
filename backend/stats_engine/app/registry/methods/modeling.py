from app.registry.schemas import MethodFiche, MethodParameter, MethodOutput

def _common_inputs():
    return {
        "X": MethodParameter(type="array<float>", description="Feature matrix (samples × features)"),
        "y": MethodParameter(type="array<float>", description="Target vector"),
    }

LOGREG_FICHE = MethodFiche(
    id="logistic_regression",
    name="Régression logistique",
    category="modeling",
    description="Classification binaire ou multinomiale via régression logistique.",
    inputs={**_common_inputs(), "C": MethodParameter(type="float", description="Inverse de la pénalité L2"), "max_iter": MethodParameter(type="int", description="Itérations maximales"), },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={"predictions": MethodOutput(type="array<int>", description="Étiquettes prédites"), "coefficients": MethodOutput(type="array<float>", description="Coefficients du modèle"), "intercept": MethodOutput(type="array<float>", description="Intercept"), "accuracy": MethodOutput(type="float", description="Score d'exactitude"),},
    numerical_method="modeling.logistic_regression",
    limitations=["Suppose que les classes sont séparables linéairement"],
    references=["Hosmer, D.W., Lemeshow, S. (2000). Applied Logistic Regression."]
)

GLM_FICHE = MethodFiche(
    id="glm",
    name="GLM (Régression linéaire)",
    category="modeling",
    description="Régression linéaire (famille gaussienne).",
    inputs=_common_inputs(),
    outputs={"predictions": MethodOutput(type="array<float>", description="Valeurs prédites"), "coefficients": MethodOutput(type="array<float>", description="Coefficients"), "intercept": MethodOutput(type="array<float>", description="Intercept"), "r2": MethodOutput(type="float", description="Coefficient de détermination"),},
    numerical_method="modeling.glm",
    limitations=["Suppose la normalité des résidus"],
    references=["Nelder, J.A., Wedderburn, R.W.M. (1972). Generalized Linear Models."]
)

RIDGE_FICHE = MethodFiche(
    id="ridge",
    name="Ridge Regression",
    category="modeling",
    description="Régression L2 pénalisée.",
    inputs={**_common_inputs(), "alpha": MethodParameter(type="float", description="Paramètre de pénalité L2")},
    outputs={"predictions": MethodOutput(type="array<float>", description="Valeurs prédites"), "coefficients": MethodOutput(type="array<float>", description="Coefficients"), "intercept": MethodOutput(type="array<float>", description="Intercept"), "r2": MethodOutput(type="float", description="Coefficient R²"),},
    numerical_method="modeling.ridge",
    references=["Hoerl, A.E., Kennard, R.W. (1970). Ridge Regression."]
)

LASSO_FICHE = MethodFiche(
    id="lasso",
    name="Lasso Regression",
    category="modeling",
    description="Régression L1 pénalisée, favorise la parcimonie.",
    inputs={**_common_inputs(), "alpha": MethodParameter(type="float", description="Paramètre de pénalité L1")},
    outputs={"predictions": MethodOutput(type="array<float>", description="Valeurs prédites"), "coefficients": MethodOutput(type="array<float>", description="Coefficients"), "intercept": MethodOutput(type="array<float>", description="Intercept"), "r2": MethodOutput(type="float", description="Coefficient R²"),},
    numerical_method="modeling.lasso",
    references=["Tibshirani, R. (1996). Regression Shrinkage and Selection via the Lasso."]
)

SVM_FICHE = MethodFiche(
    id="svm",
    name="Support Vector Machine",
    category="modeling",
    description="Classification avec marge maximale.",
    inputs={**_common_inputs(), "C": MethodParameter(type="float", description="Paramètre de régularisation"), "kernel": MethodParameter(type="str", description="Kernel à utiliser (rbf, linear, poly, sigmoid)")},
    outputs={"predictions": MethodOutput(type="array<int>", description="Étiquettes prédites"), "probabilities": MethodOutput(type="array<float>", description="Probabilités de classe"), "accuracy": MethodOutput(type="float", description="Exactitude"),},
    numerical_method="modeling.svm",
    references=["Cortes, C., Vapnik, V. (1995). Support-Vector Networks."]
)

TREE_FICHE = MethodFiche(
    id="decision_tree",
    name="Arbre de décision",
    category="modeling",
    description="Classificateur arborescent simple.",
    inputs={**_common_inputs(), "max_depth": MethodParameter(type="int", description="Profondeur maximale (optionnelle)")},
    outputs={"predictions": MethodOutput(type="array<int>", description="Étiquettes prédites"), "accuracy": MethodOutput(type="float", description="Exactitude"),},
    numerical_method="modeling.decision_tree",
    references=["Breiman, L., Friedman, J., Olshen, R., Stone, C. (1984). Classification and Regression Trees."]
)

RF_FICHE = MethodFiche(
    id="random_forest",
    name="Random Forest",
    category="modeling",
    description="Ensemble d’arbres de décision pour améliorer la robustesse.",
    inputs={**_common_inputs(), "n_estimators": MethodParameter(type="int", description="Nombre d’arbres"), "max_depth": MethodParameter(type="int", description="Profondeur maximale (optionnelle)" )},
    outputs={"predictions": MethodOutput(type="array<int>", description="Étiquettes prédites"), "accuracy": MethodOutput(type="float", description="Exactitude"),},
    numerical_method="modeling.random_forest",
    references=["Breiman, L. (2001). Random Forests."]
)

XGB_FICHE = MethodFiche(
    id="xgboost_boosting",
    name="XGBoost Boosting",
    category="modeling",
    description="Gradient boosting tree‑based classifier.",
    inputs={**_common_inputs(), "n_estimators": MethodParameter(type="int", description="Nombre d’estimateurs"), "learning_rate": MethodParameter(type="float", description="Taux d’apprentissage"), },
    outputs={"predictions": MethodOutput(type="array<int>", description="Étiquettes prédites"), "accuracy": MethodOutput(type="float", description="Exactitude"),},
    numerical_method="modeling.xgboost_boosting",
    references=["Chen, T., Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System."]
)

MULTIVARIATE_MODELING_METHODS = {
    LOGREG_FICHE.id: LOGREG_FICHE,
    GLM_FICHE.id: GLM_FICHE,
    RIDGE_FICHE.id: RIDGE_FICHE,
    LASSO_FICHE.id: LASSO_FICHE,
    SVM_FICHE.id: SVM_FICHE,
    TREE_FICHE.id: TREE_FICHE,
    RF_FICHE.id: RF_FICHE,
    XGB_FICHE.id: XGB_FICHE,
}
