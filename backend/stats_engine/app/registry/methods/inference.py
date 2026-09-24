from app.registry.schemas import (
    MethodFiche, MethodParameter, MethodAssumption, MethodFallback, MethodOutput,
)

# ============================================================
# INTERVALLES DE CONFIANCE
# ============================================================

ci_mean_known_sigma = MethodFiche(
    id="ci_mean_known_sigma",
    name="Intervalle de Confiance — Moyenne (σ connu)",
    category="inference",
    description="Calcule l'intervalle [μ-z*σ/√n, μ+z*σ/√n] dans lequel se trouve la vraie moyenne de la population avec un certain niveau de confiance (ex: 95%). Utilise la loi Normale.",
    inputs={
        "sample_mean": MethodParameter(type="float", description="Moyenne observée dans l'échantillon (x̄)"),
        "sigma": MethodParameter(type="float", description="Écart-type de la POPULATION (connu)"),
        "n": MethodParameter(type="int", description="Taille de l'échantillon"),
        "confidence": MethodParameter(type="float", description="Niveau de confiance (ex: 0.95 pour 95%)"),
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "lower_bound": MethodOutput(type="float", description="Borne inférieure de l'intervalle"),
        "upper_bound": MethodOutput(type="float", description="Borne supérieure de l'intervalle"),
        "margin_of_error": MethodOutput(type="float", description="Marge d'erreur E = z * σ/√n"),
        "z_critical": MethodOutput(type="float", description="Valeur critique z"),
    },
    numerical_method="app.inference.ci_mean_known_sigma",
    limitations=["Nécessite que σ de la population soit connu"],
    references=[]
)

ci_mean_unknown_sigma = MethodFiche(
    id="ci_mean_unknown_sigma",
    name="Intervalle de Confiance — Moyenne (σ inconnu)",
    category="inference",
    description="Calcule l'intervalle de confiance pour la moyenne quand l'écart-type de la population est inconnu. Utilise la loi de Student avec n-1 degrés de liberté.",
    inputs={
        "sample_mean": MethodParameter(type="float", description="Moyenne observée dans l'échantillon (x̄)"),
        "sample_std": MethodParameter(type="float", description="Écart-type ESTIMÉ depuis l'échantillon (s)"),
        "n": MethodParameter(type="int", description="Taille de l'échantillon"),
        "confidence": MethodParameter(type="float", description="Niveau de confiance (ex: 0.95 pour 95%)"),
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "lower_bound": MethodOutput(type="float", description="Borne inférieure de l'intervalle"),
        "upper_bound": MethodOutput(type="float", description="Borne supérieure de l'intervalle"),
        "margin_of_error": MethodOutput(type="float", description="Marge d'erreur"),
        "t_critical": MethodOutput(type="float", description="Valeur critique t"),
    },
    numerical_method="app.inference.ci_mean_unknown_sigma",
    limitations=["Population approximativement normale, surtout si n < 30"],
    references=[]
)

ci_proportion = MethodFiche(
    id="ci_proportion",
    name="Intervalle de Confiance — Proportion",
    category="inference",
    description="Estime la vraie proportion d'une caractéristique dans une population. Ex: quelle est la proportion de clients satisfaits ? (avec une marge d'erreur de ±X%)",
    inputs={
        "p_hat": MethodParameter(type="float", description="Proportion observée dans l'échantillon (entre 0 et 1)"),
        "n": MethodParameter(type="int", description="Taille de l'échantillon"),
        "confidence": MethodParameter(type="float", description="Niveau de confiance (ex: 0.95)"),
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "lower_bound": MethodOutput(type="float", description="Borne inférieure de l'intervalle"),
        "upper_bound": MethodOutput(type="float", description="Borne supérieure de l'intervalle"),
        "margin_of_error": MethodOutput(type="float", description="Marge d'erreur"),
    },
    numerical_method="app.inference.ci_proportion",
    limitations=["Nécessite n*p >= 5 et n*(1-p) >= 5"],
    references=[]
)

# ============================================================
# TESTS DE PROPORTION
# ============================================================

z_test_one_proportion = MethodFiche(
    id="z_test_one_proportion",
    name="Test Z — Proportion (un échantillon)",
    category="inference",
    description="Teste si une proportion observée est significativement différente d'une valeur de référence. Ex: le taux de réussite a-t-il changé par rapport à l'an dernier ?",
    inputs={
        "p_hat": MethodParameter(type="float", description="Proportion observée"),
        "p0": MethodParameter(type="float", description="Proportion de référence (hypothèse nulle H0)"),
        "n": MethodParameter(type="int", description="Taille de l'échantillon"),
        "alternative": MethodParameter(type="str", description="'two-sided', 'greater' ou 'less'"),
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "z_statistic": MethodOutput(type="float", description="Statistique Z calculée"),
        "p_value": MethodOutput(type="float", description="P-value du test"),
        "reject_h0": MethodOutput(type="bool", description="True si on rejette H0 au seuil α=0.05"),
    },
    numerical_method="app.inference.z_test_proportion",
    limitations=["n*p0 >= 5 et n*(1-p0) >= 5"],
    references=[]
)

z_test_two_proportions = MethodFiche(
    id="z_test_two_proportions",
    name="Test Z — Comparaison de Deux Proportions",
    category="inference",
    description="Teste si deux proportions sont significativement différentes. Ex: est-ce que le taux de satisfaction est différent entre les hommes et les femmes ?",
    inputs={
        "p1_hat": MethodParameter(type="float", description="Proportion du groupe 1"),
        "n1": MethodParameter(type="int", description="Taille de l'échantillon 1"),
        "p2_hat": MethodParameter(type="float", description="Proportion du groupe 2"),
        "n2": MethodParameter(type="int", description="Taille de l'échantillon 2"),
        "alternative": MethodParameter(type="str", description="'two-sided', 'greater' ou 'less'"),
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "z_statistic": MethodOutput(type="float", description="Statistique Z calculée"),
        "p_value": MethodOutput(type="float", description="P-value du test"),
        "reject_h0": MethodOutput(type="bool", description="True si on rejette H0"),
    },
    numerical_method="app.inference.z_test_two_proportions",
    limitations=["Les deux échantillons doivent être indépendants"],
    references=[]
)

# ============================================================
# TESTS SUPPLEMENTAIRES
# ============================================================

paired_t_test = MethodFiche(
    id="paired_t_test",
    name="Test t de Student (Échantillons Appariés)",
    category="inference",
    description="Compare les moyennes de deux groupes LIÉS (avant/après traitement, mesures sur les mêmes individus). Ex: comparer les notes avant et après une formation.",
    inputs={
        "group_before": MethodParameter(type="array<float>", description="Mesures avant (groupe 1)"),
        "group_after": MethodParameter(type="array<float>", description="Mesures après (groupe 2, même ordre)"),
    },
    assumptions=[
        MethodAssumption(id="normality", name="Normalité des différences", test_method="shapiro_wilk",
                        description="Les différences (avant - après) doivent être normalement distribuées.")
    ],
    fallback_if_assumptions_fail=[
        MethodFallback(failed_assumption="normality", fallback_method="wilcoxon_signed_rank")
    ],
    outputs={
        "statistic": MethodOutput(type="float", description="Statistique t"),
        "p_value": MethodOutput(type="float", description="P-value du test"),
        "mean_difference": MethodOutput(type="float", description="Différence moyenne observée"),
    },
    numerical_method="scipy.stats.ttest_rel",
    limitations=["Les paires doivent être liées entre elles (même individu, même unité)"],
    references=[]
)

wilcoxon = MethodFiche(
    id="wilcoxon_signed_rank",
    name="Test de Wilcoxon (Signé des Rangs)",
    category="inference",
    description="Alternative non-paramétrique au test t apparié. Utilisé quand la normalité des différences n'est pas vérifiée.",
    inputs={
        "group_before": MethodParameter(type="array<float>", description="Mesures avant"),
        "group_after": MethodParameter(type="array<float>", description="Mesures après"),
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "statistic": MethodOutput(type="float", description="Statistique W de Wilcoxon"),
        "p_value": MethodOutput(type="float", description="P-value du test"),
    },
    numerical_method="scipy.stats.wilcoxon",
    limitations=[],
    references=["Wilcoxon, F. (1945). Individual comparisons by ranking methods."]
)

ks_test = MethodFiche(
    id="kolmogorov_smirnov_test",
    name="Test de Kolmogorov-Smirnov (Normalité)",
    category="inference",
    description="Alternative au Shapiro-Wilk pour tester la normalité sur de grands échantillons (N > 50). Teste si les données suivent une distribution théorique donnée.",
    inputs={
        "data": MethodParameter(type="array<float>", description="Données à tester"),
        "distribution": MethodParameter(type="str", description="Distribution théorique ('norm', 'expon', 'uniform')"),
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "statistic": MethodOutput(type="float", description="Statistique D de KS"),
        "p_value": MethodOutput(type="float", description="P-value (si p > 0.05, la distribution est plausible)"),
        "is_normal": MethodOutput(type="bool", description="True si p >= 0.05"),
    },
    numerical_method="scipy.stats.kstest",
    limitations=["Moins puissant que Shapiro-Wilk sur petits échantillons"],
    references=["Kolmogorov, A. (1933)."]
)

INFERENCE_METHODS = {
    ci_mean_known_sigma.id: ci_mean_known_sigma,
    ci_mean_unknown_sigma.id: ci_mean_unknown_sigma,
    ci_proportion.id: ci_proportion,
    z_test_one_proportion.id: z_test_one_proportion,
    z_test_two_proportions.id: z_test_two_proportions,
    paired_t_test.id: paired_t_test,
    wilcoxon.id: wilcoxon,
    ks_test.id: ks_test,
}
