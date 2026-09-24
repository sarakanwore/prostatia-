# -*- coding: utf-8 -*-
"""advanced_stats
MethodFiche definitions for the advanced statistical utilities implemented in
`app/services/stats_advanced.py`.
"""

from typing import Dict

from app.registry.schemas import MethodFiche, MethodParameter, MethodOutput

# ---------------------------------------------------------------------------
# Skewness
# ---------------------------------------------------------------------------
SKEWNESS_FICHE = MethodFiche(
    id="skewness",
    name="Skewness (Fisher)",
    category="advanced_stats",
    description="Calcul de l'asymétrie d'une distribution (définition de Fisher).",
    inputs={
        "data": MethodParameter(type="array<float>", description="Échantillon de données"),
        "bias": MethodParameter(type="bool", description="Si True, utilise la formule biaisée (défaut = False)")
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={"skewness": MethodOutput(type="float", description="Valeur de skewness")},
    numerical_method="stats_advanced.skewness",
    limitations=[],
    references=["https://en.wikipedia.org/wiki/Skewness"]
)

# ---------------------------------------------------------------------------
# Kurtosis
# ---------------------------------------------------------------------------
KURTOSIS_FICHE = MethodFiche(
    id="kurtosis",
    name="Kurtosis (excess, Fisher)",
    category="advanced_stats",
    description="Calcul de l'excès de kurtosis d'une distribution (définition de Fisher).",
    inputs={
        "data": MethodParameter(type="array<float>", description="Échantillon de données"),
        "bias": MethodParameter(type="bool", description="Si True, utilise la formule biaisée (défaut = False)")
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={"kurtosis": MethodOutput(type="float", description="Valeur d'excès de kurtosis")},
    numerical_method="stats_advanced.kurtosis",
    limitations=[],
    references=["https://en.wikipedia.org/wiki/Kurtosis"]
)

# ---------------------------------------------------------------------------
# Proportion test (two‑sample)
# ---------------------------------------------------------------------------
PROPORTION_TEST_FICHE = MethodFiche(
    id="proportion_test",
    name="Test de proportion à deux échantillons",
    category="advanced_stats",
    description="Test de différence de proportions entre deux groupes (approximation normale).",
    inputs={
        "success_a": MethodParameter(type="int", description="Nombre de succès du groupe A"),
        "n_a": MethodParameter(type="int", description="Taille du groupe A"),
        "success_b": MethodParameter(type="int", description="Nombre de succès du groupe B"),
        "n_b": MethodParameter(type="int", description="Taille du groupe B"),
        "alternative": MethodParameter(type="str", description="'two-sided', 'larger' ou 'smaller'")
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "z": MethodOutput(type="float", description="Statistique Z"),
        "p_value": MethodOutput(type="float", description="Valeur‑p du test")
    },
    numerical_method="stats_advanced.proportion_test",
    limitations=["Approximation normale, nécessite des effectifs suffisants"],
    references=["https://en.wikipedia.org/wiki/Z-test#Two-sample_Z-test"]
)

# ---------------------------------------------------------------------------
# One‑way ANOVA
# ---------------------------------------------------------------------------
ANOVA_ONEWAY_FICHE = MethodFiche(
    id="anova_oneway",
    name="ANOVA à un facteur",
    category="advanced_stats",
    description="Analyse de variance à un facteur pour comparer les moyennes de plusieurs groupes.",
    inputs={
        # les groupes sont fournis dynamiquement avec des clés group_1, group_2, …
        "group_1": MethodParameter(type="array<float>", description="Échantillon du groupe 1"),
        "group_2": MethodParameter(type="array<float>", description="Échantillon du groupe 2"),
        # l'utilisateur peut ajouter davantage de groupes (group_3, …) – ils seront reconnus automatiquement.
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "F": MethodOutput(type="float", description="Statistique F"),
        "p_value": MethodOutput(type="float", description="Valeur‑p du test")
    },
    numerical_method="stats_advanced.anova_oneway",
    limitations=["Suppose normalité et homogénéité des variances – tester avec les validateurs appropriés"],
    references=["https://en.wikipedia.org/wiki/Analysis_of_variance"]
)

# Exported dictionary for the registry
ADVANCED_STATS_METHODS: Dict[str, MethodFiche] = {
    SKEWNESS_FICHE.id: SKEWNESS_FICHE,
    KURTOSIS_FICHE.id: KURTOSIS_FICHE,
    PROPORTION_TEST_FICHE.id: PROPORTION_TEST_FICHE,
    ANOVA_ONEWAY_FICHE.id: ANOVA_ONEWAY_FICHE,
}
