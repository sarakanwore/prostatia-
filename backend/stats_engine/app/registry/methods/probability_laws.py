from app.registry.schemas import (
    MethodFiche, MethodParameter, MethodOutput,
)

# ============================================================
# LOIS DE PROBABILITE DISCRETES
# ============================================================

binomial = MethodFiche(
    id="binomial_distribution",
    name="Loi Binomiale B(n, p)",
    category="probability_laws",
    description="Modélise le nombre de succès k dans n épreuves de Bernoulli indépendantes, chacune avec une probabilité de succès p. Ex: nombre de pièces tombant sur face en n lancers.",
    inputs={
        "n": MethodParameter(type="int", description="Nombre d'épreuves"),
        "p": MethodParameter(type="float", description="Probabilité de succès par épreuve (entre 0 et 1)"),
        "k": MethodParameter(type="int", description="Valeur observée (nombre de succès souhaité)"),
        "query_type": MethodParameter(type="str", description="Type de calcul: 'pmf' P(X=k), 'cdf' P(X<=k), 'sf' P(X>k), 'stats' pour moyenne/variance"),
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "probability": MethodOutput(type="float", description="Probabilité calculée"),
        "mean": MethodOutput(type="float", description="Espérance E[X] = n*p"),
        "variance": MethodOutput(type="float", description="Variance Var[X] = n*p*(1-p)"),
        "std_dev": MethodOutput(type="float", description="Écart-type"),
    },
    numerical_method="scipy.stats.binom",
    limitations=["Nécessite des épreuves indépendantes et p constant"],
    references=["Bernoulli, J. (1713). Ars Conjectandi."]
)

poisson = MethodFiche(
    id="poisson_distribution",
    name="Loi de Poisson P(λ)",
    category="probability_laws",
    description="Modélise le nombre d'événements rares se produisant dans un intervalle de temps/espace fixé. Ex: nombre d'appels reçus par heure, nombre de pannes par jour.",
    inputs={
        "lam": MethodParameter(type="float", description="Lambda (λ) : taux moyen d'occurrences sur l'intervalle"),
        "k": MethodParameter(type="int", description="Nombre d'occurrences observé"),
        "query_type": MethodParameter(type="str", description="Type de calcul: 'pmf', 'cdf', 'sf', 'stats'"),
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "probability": MethodOutput(type="float", description="Probabilité calculée"),
        "mean": MethodOutput(type="float", description="Espérance E[X] = λ"),
        "variance": MethodOutput(type="float", description="Variance Var[X] = λ"),
    },
    numerical_method="scipy.stats.poisson",
    limitations=["Les événements doivent être indépendants et rares"],
    references=["Poisson, S.D. (1837). Recherches sur la probabilité des jugements."]
)

hypergeometric = MethodFiche(
    id="hypergeometric_distribution",
    name="Loi Hypergéométrique H(N, K, n)",
    category="probability_laws",
    description="Modélise le nombre de succès dans un échantillon de taille n tiré SANS remise d'une population de N éléments dont K sont des 'succès'. Ex: tirage d'urne sans remise.",
    inputs={
        "N": MethodParameter(type="int", description="Taille de la population totale"),
        "K": MethodParameter(type="int", description="Nombre de 'succès' dans la population"),
        "n": MethodParameter(type="int", description="Taille de l'échantillon tiré"),
        "k": MethodParameter(type="int", description="Nombre de succès observés dans l'échantillon"),
        "query_type": MethodParameter(type="str", description="Type de calcul: 'pmf', 'cdf', 'sf', 'stats'"),
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "probability": MethodOutput(type="float", description="Probabilité calculée"),
        "mean": MethodOutput(type="float", description="Espérance E[X] = n*K/N"),
        "variance": MethodOutput(type="float", description="Variance"),
    },
    numerical_method="scipy.stats.hypergeom",
    limitations=["Tirage sans remise uniquement"],
    references=["Wallenius, K.T. (1963). Biased Sampling."]
)

geometric = MethodFiche(
    id="geometric_distribution",
    name="Loi Géométrique G(p)",
    category="probability_laws",
    description="Modélise le nombre d'épreuves nécessaires pour obtenir le premier succès. Ex: combien de coups faut-il tirer pour marquer un but ?",
    inputs={
        "p": MethodParameter(type="float", description="Probabilité de succès par épreuve"),
        "k": MethodParameter(type="int", description="Rang du premier succès"),
        "query_type": MethodParameter(type="str", description="Type de calcul: 'pmf', 'cdf', 'sf', 'stats'"),
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "probability": MethodOutput(type="float", description="Probabilité calculée"),
        "mean": MethodOutput(type="float", description="Espérance E[X] = 1/p"),
        "variance": MethodOutput(type="float", description="Variance Var[X] = (1-p)/p²"),
    },
    numerical_method="scipy.stats.geom",
    limitations=["Épreuves indépendantes avec p constant"],
    references=[]
)

# ============================================================
# LOIS DE PROBABILITE CONTINUES
# ============================================================

normal = MethodFiche(
    id="normal_distribution",
    name="Loi Normale N(μ, σ²)",
    category="probability_laws",
    description="La loi de probabilité continue la plus importante en statistique. Modélise de nombreux phénomènes naturels (tailles, erreurs de mesure, scores). La courbe en cloche de Gauss.",
    inputs={
        "mu": MethodParameter(type="float", description="Moyenne μ (centre de la distribution)"),
        "sigma": MethodParameter(type="float", description="Écart-type σ (largeur de la courbe, > 0)"),
        "x": MethodParameter(type="float", description="Valeur observée"),
        "query_type": MethodParameter(type="str", description="Type: 'cdf' P(X<=x), 'sf' P(X>x), 'pdf' densité en x, 'ppf' quantile (x est alors une probabilité entre 0 et 1), 'interval' P(a<=X<=b) — dans ce cas fournir x_low et x_high, 'stats'"),
        "x_low": MethodParameter(type="float", description="Borne inférieure pour l'intervalle (optionnel)"),
        "x_high": MethodParameter(type="float", description="Borne supérieure pour l'intervalle (optionnel)"),
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "probability": MethodOutput(type="float", description="Probabilité calculée"),
        "z_score": MethodOutput(type="float", description="Score Z standardisé de x"),
        "mean": MethodOutput(type="float", description="Espérance = μ"),
        "variance": MethodOutput(type="float", description="Variance = σ²"),
    },
    numerical_method="scipy.stats.norm",
    limitations=["La distribution doit être symétrique et en forme de cloche"],
    references=["Gauss, C.F. (1809). Theoria Motus Corporum Coelestium."]
)

student_t = MethodFiche(
    id="student_t_distribution",
    name="Loi de Student t(ν)",
    category="probability_laws",
    description="Similaire à la loi normale mais avec des queues plus épaisses. Utilisée quand l'écart-type de la population est inconnu et l'échantillon petit (N < 30).",
    inputs={
        "df": MethodParameter(type="float", description="Degrés de liberté ν (souvent N-1)"),
        "t": MethodParameter(type="float", description="Valeur de t calculée"),
        "query_type": MethodParameter(type="str", description="Type: 'cdf', 'sf', 'ppf', 'pdf', 'stats'"),
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "probability": MethodOutput(type="float", description="Probabilité calculée / p-value"),
        "critical_value": MethodOutput(type="float", description="Valeur critique t pour le seuil alpha donné"),
    },
    numerical_method="scipy.stats.t",
    limitations=["La population doit être approximativement normale"],
    references=["Student (W.S. Gosset) (1908). The probable error of a mean."]
)

chi2_dist = MethodFiche(
    id="chi2_distribution",
    name="Loi du Khi-Deux χ²(ν)",
    category="probability_laws",
    description="Utilisée pour les tests d'indépendance et d'adéquation. C'est la somme du carré de variables normales centrées réduites. Utile pour tester la variance d'une population.",
    inputs={
        "df": MethodParameter(type="float", description="Degrés de liberté ν"),
        "x": MethodParameter(type="float", description="Valeur de χ² calculée"),
        "query_type": MethodParameter(type="str", description="Type: 'cdf', 'sf', 'ppf', 'pdf', 'stats'"),
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "probability": MethodOutput(type="float", description="Probabilité calculée"),
        "critical_value": MethodOutput(type="float", description="Valeur critique χ² pour le seuil alpha donné"),
    },
    numerical_method="scipy.stats.chi2",
    limitations=["Valeurs strictement positives uniquement"],
    references=["Pearson, K. (1900)."]
)

fisher_f = MethodFiche(
    id="fisher_f_distribution",
    name="Loi de Fisher F(d1, d2)",
    category="probability_laws",
    description="Utilisée en ANOVA et pour comparer deux variances. C'est le rapport de deux variables du Khi-Deux divisées par leurs degrés de liberté.",
    inputs={
        "dfn": MethodParameter(type="float", description="Degrés de liberté du numérateur"),
        "dfd": MethodParameter(type="float", description="Degrés de liberté du dénominateur"),
        "f": MethodParameter(type="float", description="Valeur de F calculée"),
        "query_type": MethodParameter(type="str", description="Type: 'cdf', 'sf', 'ppf', 'pdf', 'stats'"),
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "probability": MethodOutput(type="float", description="Probabilité calculée / p-value"),
        "critical_value": MethodOutput(type="float", description="Valeur critique F"),
    },
    numerical_method="scipy.stats.f",
    limitations=["Valeurs strictement positives"],
    references=["Fisher, R.A. (1925). Statistical Methods for Research Workers."]
)

exponential = MethodFiche(
    id="exponential_distribution",
    name="Loi Exponentielle Exp(λ)",
    category="probability_laws",
    description="Modélise le temps d'attente entre deux événements d'un processus de Poisson. Ex: durée de vie d'un composant électronique, temps entre deux pannes.",
    inputs={
        "lam": MethodParameter(type="float", description="Taux d'occurrence λ (inverse de la moyenne)"),
        "x": MethodParameter(type="float", description="Valeur observée (temps, durée)"),
        "query_type": MethodParameter(type="str", description="Type: 'cdf', 'sf', 'pdf', 'ppf', 'stats'"),
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "probability": MethodOutput(type="float", description="Probabilité calculée"),
        "mean": MethodOutput(type="float", description="Espérance E[X] = 1/λ"),
        "variance": MethodOutput(type="float", description="Variance Var[X] = 1/λ²"),
    },
    numerical_method="scipy.stats.expon",
    limitations=["Suppose des événements indépendants (sans mémoire)"],
    references=[]
)

uniform_continuous = MethodFiche(
    id="uniform_distribution",
    name="Loi Uniforme Continue U(a, b)",
    category="probability_laws",
    description="Tous les intervalles de même longueur ont la même probabilité. Ex: arrondi de mesure, tirage aléatoire d'un nombre entre a et b.",
    inputs={
        "a": MethodParameter(type="float", description="Borne inférieure"),
        "b": MethodParameter(type="float", description="Borne supérieure"),
        "x": MethodParameter(type="float", description="Valeur observée"),
        "query_type": MethodParameter(type="str", description="Type: 'cdf', 'sf', 'pdf', 'ppf', 'stats'"),
    },
    assumptions=[],
    fallback_if_assumptions_fail=[],
    outputs={
        "probability": MethodOutput(type="float", description="Probabilité calculée"),
        "mean": MethodOutput(type="float", description="Espérance E[X] = (a+b)/2"),
        "variance": MethodOutput(type="float", description="Variance Var[X] = (b-a)²/12"),
    },
    numerical_method="scipy.stats.uniform",
    limitations=[],
    references=[]
)

PROBABILITY_METHODS = {
    binomial.id: binomial,
    poisson.id: poisson,
    hypergeometric.id: hypergeometric,
    geometric.id: geometric,
    normal.id: normal,
    student_t.id: student_t,
    chi2_dist.id: chi2_dist,
    fisher_f.id: fisher_f,
    exponential.id: exponential,
    uniform_continuous.id: uniform_continuous,
}
