from app.registry.schemas import MethodFiche, MethodParameter, MethodOutput

COMMON_INPUTS = {
    "df": MethodParameter(type="csv", description="DataFrame in CSV format"),
}

PIPELINE_FICHE = MethodFiche(
    id="basic_pipeline",
    name="Pipeline basique",
    category="preprocessing",
    description="Imputation moyenne + normalisation",
    inputs=COMMON_INPUTS,
    outputs={
        "processed_df": MethodOutput(type="csv", description="DataFrame après transformation"),
        "heatmap": MethodOutput(type="base64", description="Heatmap PNG (optionnel)"),
        "dendrogram": MethodOutput(type="base64", description="Dendrogramme PNG (optionnel)"),
    },
    numerical_method="preprocessing.run_preprocess",
    limitations=["Fonctionne uniquement sur colonnes numériques"],
    references=["scikit-learn Pipeline", "seaborn heatmap"],
)

PREPROCESSING_METHODS = {PIPELINE_FICHE.id: PIPELINE_FICHE}
