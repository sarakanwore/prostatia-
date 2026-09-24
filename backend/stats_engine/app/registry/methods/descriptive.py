from app.registry.schemas import (
    MethodFiche,
    MethodParameter,
    MethodOutput,
)

summary_statistics = MethodFiche(
    id="summary_statistics",
    name="Statistiques descriptives de base",
    category="descriptive_stats",
    description="Calcule les statistiques descriptives de base (moyenne, médiane, écart-type, min, max, quartiles) pour une variable continue.",
    inputs={
        "data": MethodParameter(type="array<float>", description="Vecteur de données numériques continus"),
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "mean": MethodOutput(type="float", description="Moyenne arithmétique"),
        "median": MethodOutput(type="float", description="Médiane"),
        "std_dev": MethodOutput(type="float", description="Écart-type"),
        "min": MethodOutput(type="float", description="Valeur minimale"),
        "max": MethodOutput(type="float", description="Valeur maximale"),
        "q1": MethodOutput(type="float", description="Premier quartile (25ème percentile)"),
        "q3": MethodOutput(type="float", description="Troisième quartile (75ème percentile)"),
        "count": MethodOutput(type="int", description="Nombre d'observations (sans valeurs manquantes)"),
    },
    numerical_method="app.engine.executor.calculate_summary_stats",
    limitations=[],
    references=[],
)

DESCRIPTIVE_METHODS = {
    summary_statistics.id: summary_statistics,
}
