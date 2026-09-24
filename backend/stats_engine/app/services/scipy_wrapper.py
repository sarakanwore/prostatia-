"""Module d'encapsulation (wrappers) pour les calculs statistiques SciPy, NumPy, statsmodels et scikit-learn.

Ce module expose les fonctions d'exécution numériques appelées par le moteur
`StatsExecutor` de PROSTATIA, notamment:
- Tests d'hypothèses univariés et bivariés (Student, Welch, Mann-Whitney, Wilcoxon, ANOVA, Kruskal-Wallis, Chi2, Kolmogorov-Smirnov).
- Régressions linéaire simple et multiple, corrélations.
- Lois de probabilités discrètes et continues (pdf, cdf, ppf, intervalles, moments).
- Inférence statistique (intervalles de confiance pour moyennes et proportions, tests Z).
- Analyse factorielle et classification non supervisée (ACP, AFC, ACM, CAH, K-Means).
"""

import scipy.stats as stats
import numpy as np
from typing import Dict, Any

def execute_ttest_ind(group_a: np.ndarray, group_b: np.ndarray, equal_var: bool = True) -> Dict[str, Any]:
    """Exécute un test t de Student (ou Welch) pour deux échantillons indépendants.

    Args:
        group_a: Premier groupe d'observations (1D array numérique).
        group_b: Deuxième groupe d'observations (1D array numérique).
        equal_var: Si True, assume l'égalité des variances (Student standard).
            Si False, effectue la correction de Welch-Satterthwaite.

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "statistic": Statistique de test t.
            - "p_value": Valeur p associée au test bilatéral.
            - "degrees_of_freedom": Degrés de liberté du test.
    """
    res = stats.ttest_ind(group_a, group_b, equal_var=equal_var)
    
    # Degrés de liberté. 
    # Pour Student: n1 + n2 - 2
    # Pour Welch: formule complexe, renvoyé par df si disponible dans scipy > 1.11
    df = getattr(res, 'df', len(group_a) + len(group_b) - 2)
    
    return {
        "statistic": float(res.statistic),
        "p_value": float(res.pvalue),
        "degrees_of_freedom": float(df)
    }

def execute_mann_whitney_u(group_a: np.ndarray, group_b: np.ndarray) -> Dict[str, Any]:
    """Exécute un test non-paramétrique U de Mann-Whitney (Wilcoxon rank-sum).

    Args:
        group_a: Premier échantillon indépendant.
        group_b: Deuxième échantillon indépendant.

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "statistic": Statistique U de Mann-Whitney.
            - "p_value": Valeur p bilatérale.
    """
    res = stats.mannwhitneyu(group_a, group_b)
    return {
        "statistic": float(res.statistic),
        "p_value": float(res.pvalue)
    }

def execute_linregress(X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
    """Calcule une régression linéaire simple par moindres carrés ordinaires.

    Args:
        X: Variable explicative (1D array numérique).
        y: Variable dépendante à expliquer (1D array numérique).

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "slope": Pente de la droite de régression.
            - "intercept": Ordonnée à l'origine.
            - "r_squared": Coefficient de détermination R².
            - "p_value": Valeur p du test d'hypothèse sur la nullité de la pente.
    """
    res = stats.linregress(X, y)
    return {
        "slope": float(res.slope),
        "intercept": float(res.intercept),
        "r_squared": float(res.rvalue ** 2),
        "p_value": float(res.pvalue)
    }

def execute_f_oneway(groups: list) -> Dict[str, Any]:
    """Exécute une ANOVA à un facteur (analyse de variance inter-groupes).

    Args:
        groups: Liste de tableaux numériques 1D représentant chacun un groupe.

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "f_statistic": Statistique F de Fisher-Snedecor.
            - "p_value": Valeur p du test de comparaison des moyennes.
    """
    res = stats.f_oneway(*groups)
    return {
        "f_statistic": float(res.statistic),
        "p_value": float(res.pvalue)
    }

def execute_kruskal(groups: list) -> Dict[str, Any]:
    """Exécute un test H de Kruskal-Wallis (ANOVA non paramétrique à un facteur).

    Args:
        groups: Liste de tableaux numériques 1D représentant chacun un groupe.

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "statistic": Statistique H de Kruskal-Wallis.
            - "p_value": Valeur p du test.
    """
    res = stats.kruskal(*groups)
    return {
        "statistic": float(res.statistic),
        "p_value": float(res.pvalue)
    }

def execute_chi2_contingency(contingency_table: list) -> Dict[str, Any]:
    """Exécute un test du Chi-carré d'indépendance sur une table de contingence.

    Args:
        contingency_table: Tableau 2D (liste de listes ou ndarray) d'effectifs observés.

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "chi2": Valeur de la statistique Chi-carré.
            - "p_value": Valeur p d'indépendance.
            - "dof": Degrés de liberté (lignes - 1) * (colonnes - 1).
            - "expected_freqs": Tableau des effectifs théoriques attendus.
    """
    res = stats.chi2_contingency(contingency_table)
    return {
        "chi2": float(res.statistic),
        "p_value": float(res.pvalue),
        "dof": int(res.dof),
        "expected_freqs": res.expected_freq.tolist()
    }

def execute_pearsonr(x: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
    """Calcule le coefficient de corrélation linéaire de Pearson entre deux variables.

    Args:
        x: Première variable continue (1D array numérique).
        y: Deuxième variable continue (1D array numérique).

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "correlation_coefficient": Coefficient r de Pearson [-1, 1].
            - "p_value": Valeur p du test de nullité de la corrélation.
    """
    res = stats.pearsonr(x, y)
    return {
        "correlation_coefficient": float(res.statistic),
        "p_value": float(res.pvalue)
    }

def execute_summary_stats(data: np.ndarray) -> Dict[str, Any]:
    """Calcule un ensemble complet de statistiques descriptives univariées.

    Args:
        data: Vecteur de données numériques (les valeurs NaN sont exclues automatiquement).

    Returns:
        Dict[str, Any]: Dictionnaire contenant moyenne, médiane, écart-type non biaisé,
        min, max, premier quartile (q1), troisième quartile (q3) et effectif valide (count).
    """
    data = data[~np.isnan(data)] # Drop NaNs
    return {
        "mean": float(np.mean(data)),
        "median": float(np.median(data)),
        "std_dev": float(np.std(data, ddof=1)),
        "min": float(np.min(data)),
        "max": float(np.max(data)),
        "q1": float(np.percentile(data, 25)),
        "q3": float(np.percentile(data, 75)),
        "count": int(len(data))
    }

def execute_multiple_linear_regression(X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
    """Ajuste une régression linéaire multiple par les moindres carrés (statsmodels OLS).

    Args:
        X: Matrice des variables explicatives (2D array numérique).
        y: Vecteur de la variable dépendante continue (1D array numérique).

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "r_squared": Coefficient de détermination R².
            - "adj_r_squared": R² ajusté pour le nombre de régresseurs.
            - "f_statistic": Statistique F globale du modèle.
            - "p_value": Valeur p globale du test F.
            - "coefficients": Liste des coefficients estimés (hors constante).
            - "intercept": Ordonnée à l'origine (constante).
    """
    import statsmodels.api as sm
    X_sm = sm.add_constant(X)
    model = sm.OLS(y, X_sm).fit()
    return {
        "r_squared": float(model.rsquared),
        "adj_r_squared": float(model.rsquared_adj),
        "f_statistic": float(model.fvalue),
        "p_value": float(model.f_pvalue),
        "coefficients": model.params[1:].tolist(),
        "intercept": float(model.params[0])
    }


# ============================================================
# ACP (Analyse en Composantes Principales)
# ============================================================
def execute_pca(data: np.ndarray) -> Dict[str, Any]:
    """Exécute une Analyse en Composantes Principales (ACP) normée.

    Les données sont automatiquement standardisées (centrées-réduites) au préalable.

    Args:
        data: Matrice d'observations numériques (2D array).

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "eigenvalues": Valeurs propres associées à chaque axe.
            - "explained_variance_ratio": Pourcentage de variance expliquée par axe.
            - "variable_correlations": Corrélations variables-composantes (cercle des corrélations).
            - "individual_coordinates": Coordonnées factorielles des individus.
    """
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    pca = PCA()
    pca.fit(data_scaled)
    individual_coords = pca.transform(data_scaled)
    correlations = pca.components_.T * np.sqrt(pca.explained_variance_)
    return {
        "eigenvalues": pca.explained_variance_.tolist(),
        "explained_variance_ratio": (pca.explained_variance_ratio_ * 100).tolist(),
        "variable_correlations": correlations.tolist(),
        "individual_coordinates": individual_coords.tolist()
    }

# ============================================================
# LOIS DE PROBABILITE
# ============================================================

def _dispatch_distribution(dist, query_type: str, x=None, x_low=None, x_high=None) -> Dict[str, Any]:
    """Interroge une loi de probabilité SciPy selon le type de calcul demandé.

    Args:
        dist: Instance de distribution aléatoire SciPy (norm, binom, t, etc.).
        query_type: Type de requête ('pdf', 'pmf', 'cdf', 'sf', 'ppf', 'interval').
        x: Point d'évaluation pour la densité, répartition ou quantile.
        x_low: Borne inférieure pour l'intervalle.
        x_high: Borne supérieure pour l'intervalle.

    Returns:
        Dict[str, Any]: Probabilité ou quantile calculé, et moments de la distribution.
    """
    result: Dict[str, Any] = {}
    if query_type == "pmf" and hasattr(dist, "pmf"):
        result["probability"] = float(dist.pmf(x))
    elif query_type == "pdf" and hasattr(dist, "pdf"):
        result["probability"] = float(dist.pdf(x))
    elif query_type == "cdf":
        result["probability"] = float(dist.cdf(x))
    elif query_type == "sf":
        result["probability"] = float(dist.sf(x))
    elif query_type == "ppf":
        result["quantile"] = float(dist.ppf(x))
    elif query_type == "interval":
        p_low = float(dist.cdf(x_low)) if x_low is not None else 0.0
        p_high = float(dist.cdf(x_high)) if x_high is not None else 1.0
        result["probability"] = round(p_high - p_low, 6)
    mean, var = dist.stats(moments="mv")
    result["mean"] = float(mean)
    result["variance"] = float(var)
    result["std_dev"] = float(var ** 0.5)
    return result


def execute_normal(mu: float, sigma: float, x: float = 0.0, query_type: str = "cdf", x_low: float = None, x_high: float = None) -> Dict[str, Any]:
    """Évalue la loi normale continue N(mu, sigma).

    Args:
        mu: Moyenne (espérance) de la distribution.
        sigma: Écart-type (> 0).
        x: Point d'évaluation pour pdf, cdf ou ppf (défaut: 0.0).
        query_type: Type de calcul ('pdf', 'cdf', 'sf', 'ppf', 'interval').
        x_low: Borne inférieure pour un calcul d'intervalle.
        x_high: Borne supérieure pour un calcul d'intervalle.

    Returns:
        Dict[str, Any]: Probabilité/quantile calculé, moments et z-score si applicable.
    """
    from scipy import stats
    dist = stats.norm(loc=mu, scale=sigma)
    result = _dispatch_distribution(dist, query_type, x=x, x_low=x_low, x_high=x_high)
    if x is not None and query_type not in ["interval", "ppf"]:
        result["z_score"] = round((x - mu) / sigma, 4)
    return result

def execute_binomial(n: int, p: float, k: int = 0, query_type: str = "pmf") -> Dict[str, Any]:
    """Évalue la loi binomiale discrète B(n, p).

    Args:
        n: Nombre total d'essais indépendants de Bernoulli (n >= 1).
        p: Probabilité de succès à chaque épreuve (0 <= p <= 1).
        k: Nombre de succès évalué (défaut: 0).
        query_type: Type de calcul ('pmf', 'cdf', 'sf', 'ppf').

    Returns:
        Dict[str, Any]: Probabilité calculée et moments théoriques.
    """
    from scipy import stats
    return _dispatch_distribution(stats.binom(n=int(n), p=p), query_type, x=int(k))

def execute_poisson(lam: float, k: int = 0, query_type: str = "pmf") -> Dict[str, Any]:
    """Évalue la loi de Poisson Pois(lambda).

    Args:
        lam: Paramètre de taux d'occurrence moyen lambda (> 0).
        k: Nombre d'occurrences évalué (défaut: 0).
        query_type: Type de calcul ('pmf', 'cdf', 'sf', 'ppf').

    Returns:
        Dict[str, Any]: Probabilité calculée et moments théoriques.
    """
    from scipy import stats
    return _dispatch_distribution(stats.poisson(mu=lam), query_type, x=int(k))

def execute_hypergeom(N: int, K: int, n: int, k: int = 0, query_type: str = "pmf") -> Dict[str, Any]:
    """Évalue la loi hypergéométrique (tirages sans remise).

    Args:
        N: Taille totale de la population.
        K: Nombre d'éléments favorables dans la population.
        n: Taille de l'échantillon extrait sans remise.
        k: Nombre de succès observés dans l'échantillon.
        query_type: Type de calcul ('pmf', 'cdf', 'sf', 'ppf').

    Returns:
        Dict[str, Any]: Probabilité calculée et moments théoriques.
    """
    from scipy import stats
    return _dispatch_distribution(stats.hypergeom(M=int(N), n=int(K), N=int(n)), query_type, x=int(k))

def execute_geometric(p: float, k: int = 1, query_type: str = "pmf") -> Dict[str, Any]:
    """Évalue la loi géométrique (nombre d'essais jusqu'au premier succès).

    Args:
        p: Probabilité de succès à chaque essai (0 < p <= 1).
        k: Rang du premier succès (k >= 1).
        query_type: Type de calcul ('pmf', 'cdf', 'sf', 'ppf').

    Returns:
        Dict[str, Any]: Probabilité calculée et moments théoriques.
    """
    from scipy import stats
    return _dispatch_distribution(stats.geom(p=p), query_type, x=int(k))

def execute_student_t(df: float, t: float = 0.0, query_type: str = "cdf") -> Dict[str, Any]:
    """Évalue la loi de Student t(df).

    Args:
        df: Degrés de liberté (df > 0).
        t: Abscisse ou quantile t évalué (défaut: 0.0).
        query_type: Type de calcul ('pdf', 'cdf', 'sf', 'ppf').

    Returns:
        Dict[str, Any]: Probabilité calculée et valeurs critiques à 95% (unilatérale et bilatérale).
    """
    from scipy import stats
    result = _dispatch_distribution(stats.t(df=df), query_type, x=t)
    result["critical_value_two_sided"] = float(stats.t.ppf(0.975, df=df))
    result["critical_value_one_sided"] = float(stats.t.ppf(0.95, df=df))
    return result

def execute_chi2_dist(df: float, x: float = 0.0, query_type: str = "cdf") -> Dict[str, Any]:
    """Évalue la loi du Chi-deux chi2(df).

    Args:
        df: Degrés de liberté (df > 0).
        x: Abscisse positive d'évaluation (défaut: 0.0).
        query_type: Type de calcul ('pdf', 'cdf', 'sf', 'ppf').

    Returns:
        Dict[str, Any]: Probabilité calculée et valeur critique à 95% (alpha=0.05).
    """
    from scipy import stats
    result = _dispatch_distribution(stats.chi2(df=df), query_type, x=x)
    result["critical_value"] = float(stats.chi2.ppf(0.95, df=df))
    return result

def execute_fisher_f(dfn: float, dfd: float, f: float = 0.0, query_type: str = "cdf") -> Dict[str, Any]:
    """Évalue la loi de Fisher-Snedecor F(dfn, dfd).

    Args:
        dfn: Degrés de liberté du numérateur (> 0).
        dfd: Degrés de liberté du dénominateur (> 0).
        f: Abscisse positive d'évaluation (défaut: 0.0).
        query_type: Type de calcul ('pdf', 'cdf', 'sf', 'ppf').

    Returns:
        Dict[str, Any]: Probabilité calculée et valeur critique au seuil 95%.
    """
    from scipy import stats
    result = _dispatch_distribution(stats.f(dfn=dfn, dfd=dfd), query_type, x=f)
    result["critical_value"] = float(stats.f.ppf(0.95, dfn=dfn, dfd=dfd))
    return result

def execute_exponential(lam: float, x: float = 0.0, query_type: str = "cdf") -> Dict[str, Any]:
    """Évalue la loi exponentielle continue Exp(lambda).

    Args:
        lam: Paramètre de taux d'occurrence lambda (> 0).
        x: Abscisse d'évaluation (défaut: 0.0).
        query_type: Type de calcul ('pdf', 'cdf', 'sf', 'ppf').

    Returns:
        Dict[str, Any]: Probabilité calculée et moments théoriques.
    """
    from scipy import stats
    return _dispatch_distribution(stats.expon(scale=1.0/lam), query_type, x=x)

def execute_uniform(a: float, b: float, x: float = 0.0, query_type: str = "cdf") -> Dict[str, Any]:
    """Évalue la loi uniforme continue sur l'intervalle [a, b].

    Args:
        a: Borne inférieure de l'intervalle.
        b: Borne supérieure de l'intervalle (b > a).
        x: Abscisse d'évaluation (défaut: 0.0).
        query_type: Type de calcul ('pdf', 'cdf', 'sf', 'ppf').

    Returns:
        Dict[str, Any]: Probabilité calculée et moments théoriques.
    """
    from scipy import stats
    return _dispatch_distribution(stats.uniform(loc=a, scale=b - a), query_type, x=x)

# ============================================================
# INFERENCE STATISTIQUE
# ============================================================

def execute_ci_mean_known_sigma(sample_mean: float, sigma: float, n: int, confidence: float = 0.95) -> Dict[str, Any]:
    """Calcule l'intervalle de confiance pour une moyenne avec écart-type population connu (loi normale Z).

    Args:
        sample_mean: Moyenne observée dans l'échantillon.
        sigma: Écart-type connu de la population.
        n: Taille de l'échantillon.
        confidence: Niveau de confiance (défaut: 0.95 pour 95%).

    Returns:
        Dict[str, Any]: Dictionnaire contenant lower_bound, upper_bound, margin_of_error et z_critical.
    """
    from scipy import stats
    z = float(stats.norm.ppf(1 - (1 - confidence) / 2))
    me = z * sigma / (n ** 0.5)
    return {"lower_bound": round(sample_mean - me, 4), "upper_bound": round(sample_mean + me, 4), "margin_of_error": round(me, 4), "z_critical": round(z, 4)}

def execute_ci_mean_unknown_sigma(sample_mean: float, sample_std: float, n: int, confidence: float = 0.95) -> Dict[str, Any]:
    """Calcule l'intervalle de confiance pour une moyenne avec écart-type inconnu (loi de Student).

    Args:
        sample_mean: Moyenne observée dans l'échantillon.
        sample_std: Écart-type empirique corrigé de l'échantillon.
        n: Taille de l'échantillon (n >= 2).
        confidence: Niveau de confiance (défaut: 0.95 pour 95%).

    Returns:
        Dict[str, Any]: Dictionnaire contenant lower_bound, upper_bound, margin_of_error et t_critical.
    """
    from scipy import stats
    t_crit = float(stats.t.ppf(1 - (1 - confidence) / 2, df=n - 1))
    me = t_crit * sample_std / (n ** 0.5)
    return {"lower_bound": round(sample_mean - me, 4), "upper_bound": round(sample_mean + me, 4), "margin_of_error": round(me, 4), "t_critical": round(t_crit, 4)}

def execute_ci_proportion(p_hat: float, n: int, confidence: float = 0.95) -> Dict[str, Any]:
    """Calcule l'intervalle de confiance asymptotique de Wald pour une proportion.

    Args:
        p_hat: Proportion observée dans l'échantillon (0 <= p_hat <= 1).
        n: Taille de l'échantillon.
        confidence: Niveau de confiance (défaut: 0.95).

    Returns:
        Dict[str, Any]: Dictionnaire contenant lower_bound, upper_bound et margin_of_error.
    """
    from scipy import stats
    z = float(stats.norm.ppf(1 - (1 - confidence) / 2))
    me = z * (p_hat * (1 - p_hat) / n) ** 0.5
    return {"lower_bound": round(max(0.0, p_hat - me), 4), "upper_bound": round(min(1.0, p_hat + me), 4), "margin_of_error": round(me, 4)}

def execute_z_test_proportion(p_hat: float, p0: float, n: int, alternative: str = "two-sided") -> Dict[str, Any]:
    """Exécute un test Z unilatéral ou bilatéral pour une proportion d'échantillon contre p0.

    Args:
        p_hat: Proportion empirique observée.
        p0: Valeur de référence sous l'hypothèse nulle H0.
        n: Taille de l'échantillon.
        alternative: Type d'alternative ('two-sided', 'greater', 'less').

    Returns:
        Dict[str, Any]: Statistique z, p-value et décision de rejet de H0 (alpha=0.05).
    """
    from scipy import stats
    z = (p_hat - p0) / ((p0 * (1 - p0) / n) ** 0.5)
    p_value = 2 * float(stats.norm.sf(abs(z))) if alternative == "two-sided" else float(stats.norm.sf(z) if alternative == "greater" else stats.norm.cdf(z))
    return {"z_statistic": round(float(z), 4), "p_value": round(p_value, 4), "reject_h0": p_value < 0.05}

def execute_z_test_two_proportions(p1_hat: float, n1: int, p2_hat: float, n2: int, alternative: str = "two-sided") -> Dict[str, Any]:
    """Exécute un test Z de comparaison de deux proportions indépendantes.

    Args:
        p1_hat: Proportion observée dans le premier échantillon.
        n1: Taille du premier échantillon.
        p2_hat: Proportion observée dans le second échantillon.
        n2: Taille du second échantillon.
        alternative: Type d'alternative ('two-sided', 'greater', 'less').

    Returns:
        Dict[str, Any]: Statistique z, p-value et décision de rejet de H0.
    """
    from scipy import stats
    p_pool = (p1_hat * n1 + p2_hat * n2) / (n1 + n2)
    z = (p1_hat - p2_hat) / (p_pool * (1 - p_pool) * (1/n1 + 1/n2)) ** 0.5
    p_value = 2 * float(stats.norm.sf(abs(z))) if alternative == "two-sided" else float(stats.norm.sf(z) if alternative == "greater" else stats.norm.cdf(z))
    return {"z_statistic": round(float(z), 4), "p_value": round(p_value, 4), "reject_h0": p_value < 0.05}

def execute_paired_t_test(group_before: np.ndarray, group_after: np.ndarray) -> Dict[str, Any]:
    """Exécute un test t de Student pour deux échantillons appariés (mesures répétées).

    Args:
        group_before: Observations de la première condition / avant traitement.
        group_after: Observations de la deuxième condition / après traitement.

    Returns:
        Dict[str, Any]: Statistique t, p-value bilatérale et différence moyenne estimée.
    """
    from scipy import stats
    res = stats.ttest_rel(group_before, group_after)
    return {"statistic": round(float(res.statistic), 4), "p_value": round(float(res.pvalue), 4), "mean_difference": round(float(np.mean(group_before - group_after)), 4)}

def execute_wilcoxon(group_before: np.ndarray, group_after: np.ndarray) -> Dict[str, Any]:
    """Exécute un test non paramétrique des rangs signés de Wilcoxon pour séries appariées.

    Args:
        group_before: Observations de la première condition.
        group_after: Observations de la deuxième condition.

    Returns:
        Dict[str, Any]: Statistique W de Wilcoxon et p-value.
    """
    from scipy import stats
    res = stats.wilcoxon(group_before, group_after)
    return {"statistic": round(float(res.statistic), 4), "p_value": round(float(res.pvalue), 4)}

def execute_kstest(data: np.ndarray, distribution: str = "norm") -> Dict[str, Any]:
    """Exécute un test d'adéquation de Kolmogorov-Smirnov univarié.

    Args:
        data: Vecteur numérique d'observations à tester.
        distribution: Nom de la loi théorique de référence (défaut: 'norm').

    Returns:
        Dict[str, Any]: Statistique de Kolmogorov-Smirnov, p-value et verdict de conformité.
    """
    from scipy import stats
    res = stats.kstest(data, distribution)
    return {"statistic": round(float(res.statistic), 4), "p_value": round(float(res.pvalue), 4), "is_normal": bool(res.pvalue >= 0.05)}

# ------------------------------------------------------------
# ANALYSE FACTORIELLE MULTIVARIÉE
# ------------------------------------------------------------

def execute_afc(contingency_table: list) -> Dict[str, Any]:
    """Effectue une Analyse Factorielle des Correspondances (AFC) simple à partir d'un tableau de contingence.

    Args:
        contingency_table: Matrice de contingence croisant deux variables catégorielles.

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "row_coordinates": Coordonnées factorielles des profils-lignes.
            - "col_coordinates": Coordonnées factorielles des profils-colonnes.
            - "explained_inertia": Pourcentage d'inertie expliquée par chaque axe factoriel.
    """
    import numpy as np
    from sklearn.decomposition import TruncatedSVD
    table = np.array(contingency_table, dtype=float)
    grand_total = table.sum()
    row_sums = table.sum(axis=1, keepdims=True)
    col_sums = table.sum(axis=0, keepdims=True)
    expected = row_sums @ col_sums / grand_total
    with np.errstate(divide='ignore', invalid='ignore'):
        std_residuals = (table - expected) / np.sqrt(expected)
        std_residuals[np.isnan(std_residuals)] = 0.0
    svd = TruncatedSVD(n_components=min(table.shape)-1)
    svd.fit(std_residuals)
    row_coords = svd.transform(std_residuals)
    col_coords = svd.components_.T * svd.singular_values_
    explained_inertia = svd.explained_variance_ratio_.tolist()
    return {
        "row_coordinates": row_coords.tolist(),
        "col_coordinates": col_coords.tolist(),
        "explained_inertia": explained_inertia,
    }

def execute_acm(indicator_matrix: list) -> Dict[str, Any]:
    """Effectue une Analyse des Correspondances Multiples (ACM) à partir d'une matrice indicatrice (dummy matrix).

    Args:
        indicator_matrix: Matrice binaire 0/1 représentant les modalités de variables qualitatives.

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "coordinates": Coordonnées des points dans l'espace factoriel réduit.
            - "explained_inertia": Pourcentage d'inertie expliquée par chaque axe.
    """
    import numpy as np
    from sklearn.decomposition import TruncatedSVD
    X = np.array(indicator_matrix, dtype=float)
    col_means = X.mean(axis=0, keepdims=True)
    col_std = X.std(axis=0, ddof=1, keepdims=True)
    col_std[col_std == 0] = 1.0
    X_std = (X - col_means) / col_std
    svd = TruncatedSVD(n_components=min(X_std.shape)-1)
    svd.fit(X_std)
    coordinates = svd.transform(X_std)
    explained_inertia = svd.explained_variance_ratio_.tolist()
    return {
        "coordinates": coordinates.tolist(),
        "explained_inertia": explained_inertia,
    }

def execute_cah(data: list, n_clusters: int = 2, linkage_method: str = "ward") -> Dict[str, Any]:
    """Effectue une Classification Ascendante Hiérarchique (CAH) agglomérative.

    Args:
        data: Liste de vecteurs d'observations numériques.
        n_clusters: Nombre de clusters souhaité dans la partition finale (défaut: 2).
        linkage_method: Méthode de fusion / calcul de distance ('ward', 'complete', 'average', etc.).

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "labels": Liste des affectations de chaque observation à un cluster.
            - "linkage_matrix": Matrice de liaison Z utilisée pour tracer le dendrogramme.
    """
    import numpy as np
    from scipy.cluster.hierarchy import linkage, fcluster
    X = np.array(data, dtype=float)
    Z = linkage(X, method=linkage_method)
    labels = fcluster(Z, t=n_clusters, criterion='maxclust')
    return {
        "labels": labels.tolist(),
        "linkage_matrix": Z.tolist(),
    }

def execute_kmeans(data: list, n_clusters: int = 3, max_iter: int = 300, init: str = "k-means++") -> Dict[str, Any]:
    """Partitionne les observations en k clusters à l'aide de l'algorithme K-Means.

    Args:
        data: Données numériques sous forme de liste d'échantillons.
        n_clusters: Nombre de clusters k à former (défaut: 3).
        max_iter: Nombre maximal d'itérations d'ajustement (défaut: 300).
        init: Méthode d'initialisation des centroïdes ('k-means++' ou 'random').

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "centers": Coordonnées finales des centres de gravité des clusters.
            - "labels": Affectation de chaque point à son cluster le plus proche.
            - "inertia": Somme des carrés des distances intra-cluster (inertie intra).
    """
    import numpy as np
    from sklearn.cluster import KMeans
    X = np.array(data, dtype=float)
    kmeans = KMeans(n_clusters=n_clusters, init=init, max_iter=max_iter, n_init=10, random_state=0)
    kmeans.fit(X)
    return {
        "centers": kmeans.cluster_centers_.tolist(),
        "labels": kmeans.labels_.tolist(),
        "inertia": float(kmeans.inertia_),
    }

# ============================================================
# REGISTRE GLOBAL COMPLET
# ============================================================
SCIPY_REGISTRY = {
    # Tests statistiques classiques
    "scipy.stats.ttest_ind": execute_ttest_ind,
    "scipy.stats.mannwhitneyu": execute_mann_whitney_u,
    "scipy.stats.linregress": execute_linregress,
    "scipy.stats.f_oneway": execute_f_oneway,
    "scipy.stats.chi2_contingency": execute_chi2_contingency,
    "scipy.stats.pearsonr": execute_pearsonr,
    "app.engine.executor.calculate_summary_stats": execute_summary_stats,
    "statsmodels.api.OLS": execute_multiple_linear_regression,
    "scipy.stats.kruskal": execute_kruskal,
    # Analyse Multidimensionnelle
    "sklearn.decomposition.PCA": execute_pca,
    # Lois de probabilité discrètes
    "scipy.stats.binom": execute_binomial,
    "scipy.stats.poisson": execute_poisson,
    "scipy.stats.hypergeom": execute_hypergeom,
    "scipy.stats.geom": execute_geometric,
    # Lois de probabilité continues
    "scipy.stats.norm": execute_normal,
    "scipy.stats.t": execute_student_t,
    "scipy.stats.chi2": execute_chi2_dist,
    "scipy.stats.f": execute_fisher_f,
    "scipy.stats.expon": execute_exponential,
    "scipy.stats.uniform": execute_uniform,
    # Inférence statistique
    "app.inference.ci_mean_known_sigma": execute_ci_mean_known_sigma,
    "app.inference.ci_mean_unknown_sigma": execute_ci_mean_unknown_sigma,
    "app.inference.ci_proportion": execute_ci_proportion,
    "app.inference.z_test_proportion": execute_z_test_proportion,
    "app.inference.z_test_two_proportions": execute_z_test_two_proportions,
    "scipy.stats.ttest_rel": execute_paired_t_test,
    "scipy.stats.wilcoxon": execute_wilcoxon,
    "scipy.stats.kstest": execute_kstest,
    "scipy.wrapper.execute_afc": execute_afc,
    "scipy.wrapper.execute_acm": execute_acm,
    "scipy.wrapper.execute_cah": execute_cah,
    "scipy.wrapper.execute_kmeans": execute_kmeans,
}

