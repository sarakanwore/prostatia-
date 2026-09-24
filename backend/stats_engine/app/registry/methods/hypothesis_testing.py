from app.registry.schemas import (
    MethodFiche,
    MethodParameter,
    MethodAssumption,
    MethodFallback,
    MethodOutput,
)

t_test_independent = MethodFiche(
    id="t_test_independent",
    name="Test t de Student (Échantillons Indépendants)",
    category="hypothesis_testing",
    description="Compare les moyennes de deux groupes indépendants pour déterminer si elles sont significativement différentes.",
    inputs={
        "group_a": MethodParameter(type="array<float>", description="Données du premier groupe"),
        "group_b": MethodParameter(type="array<float>", description="Données du second groupe"),
    },
    assumptions=[
        MethodAssumption(
            id="normality",
            name="Normalité",
            test_method="shapiro_wilk",
            description="Les données de chaque groupe doivent suivre une distribution normale.",
        ),
        MethodAssumption(
            id="homoscedasticity",
            name="Homogénéité des variances",
            test_method="levene",
            description="Les variances des deux groupes doivent être égales.",
        ),
    ],
    fallback_if_assumptions_fail=[
        MethodFallback(
            failed_assumption="normality", fallback_method="mann_whitney_u"
        ),
        MethodFallback(
            failed_assumption="homoscedasticity", fallback_method="welch_t_test"
        ),
    ],
    outputs={
        "statistic": MethodOutput(type="float", description="La valeur t calculée"),
        "p_value": MethodOutput(type="float", description="La probabilité critique"),
        "degrees_of_freedom": MethodOutput(type="float", description="Degrés de liberté"),
    },
    numerical_method="scipy.stats.ttest_ind",
    limitations=[
        "Sensible aux valeurs aberrantes (outliers)",
        "Nécessite que les deux échantillons soient indépendants l'un de l'autre",
    ],
    references=[
        "Student (1908). The probable error of a mean.",
        "Welch (1947). The generalization of 'Student's' problem when several different population variances are involved.",
    ],
)

# ANOVA à un facteur
anova_one_way = MethodFiche(
    id="anova_one_way",
    name="ANOVA à un facteur",
    category="hypothesis_testing",
    description="Compare les moyennes de plus de deux groupes indépendants.",
    inputs={
        "groups": MethodParameter(type="list<array<float>>", description="Liste contenant les données de chaque groupe"),
    },
    assumptions=[
        MethodAssumption(
            id="normality",
            name="Normalité des résidus",
            test_method="shapiro_wilk",
            description="Les données de chaque groupe doivent être approximativement normales."
        ),
        MethodAssumption(
            id="homoscedasticity",
            name="Homogénéité des variances",
            test_method="levene",
            description="Les variances des groupes doivent être égales."
        )
    ],
    fallback_if_assumptions_fail=[
        MethodFallback(failed_assumption="normality", fallback_method="kruskal_wallis")
    ],
    outputs={
        "f_statistic": MethodOutput(type="float", description="La statistique F"),
        "p_value": MethodOutput(type="float", description="La p-value de l'ANOVA")
    },
    numerical_method="scipy.stats.f_oneway",
    limitations=["Sensible aux grandes déviations de la normalité et des variances."],
    references=["Fisher, R. A. (1925). Statistical Methods for Research Workers."]
)

# Mann-Whitney U (Non paramétrique)
mann_whitney_u = MethodFiche(
    id="mann_whitney_u",
    name="Test U de Mann-Whitney",
    category="hypothesis_testing",
    description="Test non paramétrique alternatif au test t indépendant, utilisé quand les conditions de normalité ne sont pas remplies.",
    inputs={
        "group_a": MethodParameter(type="array<float>", description="Données du premier groupe"),
        "group_b": MethodParameter(type="array<float>", description="Données du second groupe"),
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "statistic": MethodOutput(type="float", description="La statistique U"),
        "p_value": MethodOutput(type="float", description="La p-value du test")
    },
    numerical_method="scipy.stats.mannwhitneyu",
    limitations=["Teste l'égalité des distributions, pas seulement des médianes."],
    references=["Mann, H. B., & Whitney, D. R. (1947). On a Test of Whether one of Two Random Variables is Stochastically Larger than the Other."]
)

# Test du Chi-Deux d'indépendance
chi_square_independence = MethodFiche(
    id="chi_square_independence",
    name="Test du Chi-Deux d'indépendance",
    category="hypothesis_testing",
    description="Teste l'indépendance entre deux variables catégorielles.",
    inputs={
        "contingency_table": MethodParameter(type="array<array<int>>", description="Tableau de contingence des effectifs croisés"),
    },
    assumptions=[
        MethodAssumption(
            id="expected_freq",
            name="Effectifs théoriques suffisants",
            test_method="contingency_expected_freq",
            description="Les effectifs théoriques de chaque case doivent être supérieurs ou égaux à 5."
        )
    ],
    fallback_if_assumptions_fail=[],
    outputs={
        "chi2": MethodOutput(type="float", description="Statistique du Chi-Deux"),
        "p_value": MethodOutput(type="float", description="La p-value du test"),
        "dof": MethodOutput(type="int", description="Degrés de liberté"),
        "expected_freqs": MethodOutput(type="array<array<float>>", description="Fréquences théoriques attendues")
    },
    numerical_method="scipy.stats.chi2_contingency",
    limitations=["Nécessite des effectifs théoriques suffisants (souvent > 5 par case)."],
    references=["Pearson, K. (1900). On the criterion that a given system of deviations from the probable in the case of a correlated system of variables is such that it can be reasonably supposed to have arisen from random sampling."]
)

# Corrélation de Pearson
pearson_correlation = MethodFiche(
    id="pearson_correlation",
    name="Corrélation de Pearson",
    category="hypothesis_testing",
    description="Mesure la force et la direction de la relation linéaire entre deux variables continues.",
    inputs={
        "x": MethodParameter(type="array<float>", description="Première variable continue"),
        "y": MethodParameter(type="array<float>", description="Deuxième variable continue"),
    },
    assumptions=[
        MethodAssumption(
            id="linearity",
            name="Linéarité",
            test_method="visual_check",
            description="La relation entre les deux variables doit être linéaire."
        ),
        MethodAssumption(
            id="normality",
            name="Normalité",
            test_method="shapiro_wilk",
            description="Les deux variables doivent suivre une distribution normale pour que le test de significativité soit exact."
        )
    ],
    fallback_if_assumptions_fail=[
        MethodFallback(failed_assumption="normality", fallback_method="spearman_correlation")
    ],
    outputs={
        "correlation_coefficient": MethodOutput(type="float", description="Le coefficient de corrélation r (entre -1 et 1)"),
        "p_value": MethodOutput(type="float", description="La p-value testant si la corrélation est différente de 0")
    },
    numerical_method="scipy.stats.pearsonr",
    limitations=["Ne mesure que les relations linéaires", "Très sensible aux valeurs aberrantes"],
    references=["Pearson, K. (1895). Notes on regression and inheritance in the case of two parents."]
)

# Registre local pour les tests
HYPOTHESIS_METHODS = {
    t_test_independent.id: t_test_independent,
    anova_one_way.id: anova_one_way,
    mann_whitney_u.id: mann_whitney_u,
    chi_square_independence.id: chi_square_independence,
    pearson_correlation.id: pearson_correlation,
}
