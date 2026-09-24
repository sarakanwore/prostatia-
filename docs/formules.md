# Formules et Références Mathématiques – PROSTATIA

Ce document rassemble les formulations mathématiques, conditions d'application et références algorithmiques des méthodes implémentées dans le **PROSTATIA Stats Engine** (`app.services.*`).

---

## 1. Statistiques descriptives & Moments

| Mesure / Moment | Formule mathématique | Description & Usage |
|---|---|---|
| **Moyenne empirique** | $\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$ | Tendance centrale de l'échantillon. |
| **Variance corrigée** | $s^2 = \frac{1}{n-1}\sum_{i=1}^{n} (x_i - \bar{x})^2$ | Dispersion d'échantillon non biaisée (`ddof=1`). |
| **Écart-type** | $s = \sqrt{s^2}$ | Dispersion dans l'unité d'origine des données. |
| **Quantiles / Médiane** | $Q_p = \inf\{x : F(x) \ge p\}$ | Séparation des observations (médiane $p=0.5$, quartiles $p=0.25, 0.75$). |
| **Asymétrie (Skewness de Fisher)** | $\text{skew} = \frac{\frac{1}{n}\sum_{i=1}^{n}(x_i-\bar{x})^3}{\left(\frac{1}{n}\sum_{i=1}^{n}(x_i-\bar{x})^2\right)^{3/2}}$ | Mesure de l'asymétrie de la distribution (0 pour la normale). |
| **Aplatissement (Kurtosis de Fisher)** | $\text{kurt} = \frac{\frac{1}{n}\sum_{i=1}^{n}(x_i-\bar{x})^4}{\left(\frac{1}{n}\sum_{i=1}^{n}(x_i-\bar{x})^2\right)^2} - 3$ | Excès de kurtosis (queue lourde $> 0$, queue légère $< 0$). |

---

## 2. Tests d'hypothèses

| Test | Hypothèse nulle $H_0$ | Statistique de test | Conditions d'application & Fallback |
|---|---|---|---|
| **Shapiro-Wilk** | Distribution normale | $W = \frac{\left(\sum a_i x_{(i)}\right)^2}{\sum (x_i - \bar{x})^2}$ | $n < 5000$, distribution continue. Valide les tests paramétriques. |
| **Levene** | Homogénéité des variances $\sigma_1^2 = \dots = \sigma_k^2$ | $W = \frac{N-k}{k-1} \frac{\sum n_i (\bar{z}_{i\cdot} - \bar{z}_{\cdot\cdot})^2}{\sum\sum (z_{ij} - \bar{z}_{i\cdot})^2}$ | Robuste aux non-normalités. Si rejeté $\rightarrow$ test de Welch. |
| **t-test Student (indépendant)** | $\mu_1 = \mu_2$ | $t = \frac{\bar{x}_1 - \bar{x}_2}{s_p \sqrt{1/n_1 + 1/n_2}}$ | Normalité et variances égales requises. Fallback : Mann-Whitney. |
| **t-test de Welch** | $\mu_1 = \mu_2$ | $t = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{s_1^2/n_1 + s_2^2/n_2}}$ | Variances inégales. Degrés de liberté de Welch-Satterthwaite. |
| **Mann-Whitney U** | Distributions identiques | $U = n_1 n_2 + \frac{n_1(n_1+1)}{2} - R_1$ | Non paramétrique, pas d'hypothèse de normalité requise. |
| **t-test apparié** | $\mu_D = 0$ ($D = X - Y$) | $t = \frac{\bar{d}}{s_d / \sqrt{n}}$ | Mesures répétées sur les mêmes sujets. Fallback : Wilcoxon. |
| **Wilcoxon (rangs signés)** | Médiane des différences nulle | $W = \sum \text{sgn}(d_i) \cdot \text{rank}(\|d_i\|)$ | Non paramétrique pour séries appariées. |
| **ANOVA à 1 facteur** | $\mu_1 = \dots = \mu_k$ | $F = \frac{\text{MS}_{\text{between}}}{\text{MS}_{\text{within}}}$ | Normalité et variances égales. Fallback : Kruskal-Wallis. |
| **Kruskal-Wallis** | Médianes des $k$ groupes égales | $H = \frac{12}{N(N+1)} \sum \frac{R_i^2}{n_i} - 3(N+1)$ | ANOVA non paramétrique. |
| **Chi-carré d'indépendance** | Deux variables qualitatives indépendantes | $\chi^2 = \sum \frac{(O_{ij} - E_{ij})^2}{E_{ij}}$ | Effectifs théoriques $E_{ij} \ge 5$ par case. |
| **Kolmogorov-Smirnov** | Échantillon issu de la loi $F_0$ | $D = \sup_x \|F_n(x) - F_0(x)\|$ | Variable continue, test univarié d'ajustement. |

---

## 3. Inférence & Intervalles de Confiance

| Estimateur | Niveau de confiance | Formule de l'intervalle | Remarques |
|---|---|---|---|
| **Moyenne ($\sigma$ connu)** | $1 - \alpha$ | $\left[\bar{x} - z_{\alpha/2}\frac{\sigma}{\sqrt{n}}, \quad \bar{x} + z_{\alpha/2}\frac{\sigma}{\sqrt{n}}\right]$ | Utilise la loi normale centrée réduite $Z$. |
| **Moyenne ($\sigma$ inconnu)** | $1 - \alpha$ | $\left[\bar{x} - t_{\alpha/2, n-1}\frac{s}{\sqrt{n}}, \quad \bar{x} + t_{\alpha/2, n-1}\frac{s}{\sqrt{n}}\right]$ | Utilise la loi de Student à $n-1$ ddl. |
| **Proportion (Wald)** | $1 - \alpha$ | $\left[\hat{p} - z_{\alpha/2}\sqrt{\frac{\hat{p}(1-\hat{p})}{n}}, \quad \hat{p} + z_{\alpha/2}\sqrt{\frac{\hat{p}(1-\hat{p})}{n}}\right]$ | Approximation normale valide si $n\hat{p} \ge 5$ et $n(1-\hat{p}) \ge 5$. |
| **Test Z de 2 proportions** | Bilatéral ou unilatéral | $z = \frac{\hat{p}_1 - \hat{p}_2}{\sqrt{\hat{p}_{\text{pool}}(1-\hat{p}_{\text{pool}})(1/n_1 + 1/n_2)}}$ | Avec $\hat{p}_{\text{pool}} = \frac{x_1+x_2}{n_1+n_2}$. |

---

## 4. Modélisation & Apprentissage supervisé

| Modèle | Problème d'optimisation / Formulation | Métriques principales |
|---|---|---|
| **MCO (Régression linéaire)** | $\min_\beta \|y - X\beta\|_2^2$ | $R^2$, $R^2_{\text{adj}}$, RMSE, p-values |
| **Ridge (L2)** | $\min_\beta \|y - X\beta\|_2^2 + \lambda \|\beta\|_2^2$ | $R^2$, RMSE (stabilise la colinéarité) |
| **Lasso (L1)** | $\min_\beta \|y - X\beta\|_2^2 + \lambda \|\beta\|_1$ | $R^2$, MAE (sélection de variables parcimonieuse) |
| **Régression logistique** | $p(y=1\|x) = \sigma(X\beta) = \frac{1}{1 + e^{-X\beta}}$ | Exactitude (Accuracy), Log-Loss, ROC-AUC |
| **Support Vector Classifier (SVC)** | $\max_{\beta, b} \frac{2}{\|\beta\|}$ sous contraintes de marge douce | Exactitude, F1-Score |
| **Arbre de décision** | Minimisation de l'impureté de Gini ou entropie de Shannon | Exactitude |
| **Forêts aléatoires** | Agrégation par ensachage (bagging) d'arbres décorrélés | Exactitude, importance des variables |
| **XGBoost** | Optimisation par descente de gradient avec régularisation $\Omega(f_k)$ | Exactitude, Log-loss |

---

## 5. Analyse multivariée & Clustering

| Méthode | Objectif & Formalisme mathématique |
|---|---|
| **ACP (PCA)** | Diagonalisation de la matrice de corrélation $R = V \Lambda V^T$. Projection orthogonale maximisant la variance restituée. |
| **AFC** | Décomposition en valeurs singulières des résidus standardisés d'une table de contingence : $S = D_r^{-1/2}(P - r c^T)D_c^{-1/2}$. |
| **ACM** | Analyse factorielle sur tableau disjonctif complet ou matrice de Burt pour variables qualitatives multiples. |
| **FastICA** | Séparation de sources non gaussiennes indépendantes par maximisation de la néguentropie. |
| **LDA** | Maximisation du ratio de variance inter-classes / variance intra-classes : $\max_w \frac{w^T S_B w}{w^T S_W w}$. |
| **t-SNE** | Minimisation de la divergence de Kullback-Leibler entre probabilités de voisinage en haute et basse dimensions. |
| **UMAP** | Préservation des structures locales et globales par approximation de variétés riemanniennes et ensembles flous. |
| **CAH (Ward)** | Fusion successive minimisant l'accroissement de la variance intra-classe $\Delta I = \frac{n_A n_B}{n_A + n_B} \|\bar{x}_A - \bar{x}_B\|^2$. |
| **K-Means** | Partitionnement minimisant l'inertie intra-cluster : $\min \sum_{k=1}^K \sum_{x \in C_k} \|x - \mu_k\|^2$. |
| **DBSCAN** | Agrégation des points cœurs possédant au moins `min_samples` dans un rayon $\epsilon$. Détection robuste du bruit (valeurs aberrantes). |

---

## 6. Lois de Probabilité

| Distribution | Densité $f(x)$ ou Masse $P(X=k)$ | Paramètres | Support | Usage typique |
|---|---|---|---|---|
| **Normale** (`normal`) | $f(x)=\frac{1}{\sigma\sqrt{2\pi}}\exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$ | $\mu \in \mathbb{R}$, $\sigma > 0$ | $x \in \mathbb{R}$ | Théorème central limite, erreurs de mesure |
| **Student-t** (`student_t`) | $f(t)=\frac{\Gamma((\nu+1)/2)}{\sqrt{\nu\pi}\Gamma(\nu/2)}\left(1+\frac{t^2}{\nu}\right)^{-(\nu+1)/2}$ | $\nu > 0$ (ddl) | $t \in \mathbb{R}$ | Inférence sur petits échantillons |
| **Chi-carré** (`chi2`) | $f(x)=\frac{1}{2^{k/2}\Gamma(k/2)}x^{k/2-1}e^{-x/2}$ | $k > 0$ (ddl) | $x \ge 0$ | Tests d'indépendance et d'adéquation |
| **Fisher-F** (`fisher_f`) | $f(x)=\frac{\sqrt{\frac{(d_1 x)^{d_1} d_1^{d_1} d_2^{d_2}}{(d_1 x + d_2)^{d_1+d_2}}}}{x B(d_1/2, d_2/2)}$ | $d_1, d_2 > 0$ | $x \ge 0$ | Rapports de variances, ANOVA, régression |
| **Binomiale** (`binomial`) | $P(X=k)=\binom{n}{k}p^k (1-p)^{n-k}$ | $n \in \mathbb{N}^*$, $0 \le p \le 1$ | $k \in \{0, \dots, n\}$ | Nombre de succès dans $n$ tirages indépendants |
| **Poisson** (`poisson`) | $P(X=k)=\frac{\lambda^k e^{-\lambda}}{k!}$ | $\lambda > 0$ | $k \in \mathbb{N}$ | Événements rares sur intervalle continu |
| **Hypergéométrique** (`hypergeom`) | $P(X=k)=\frac{\binom{K}{k}\binom{N-K}{n-k}}{\binom{N}{n}}$ | $N, K, n \in \mathbb{N}^*$ | $\max(0, n+K-N) \le k \le \min(K, n)$ | Tirages sans remise dans population finie |
| **Géométrique** (`geometric`) | $P(X=k)=(1-p)^{k-1}p$ | $0 < p \le 1$ | $k \in \mathbb{N}^*$ | Rang du premier succès |
| **Exponentielle** (`exponential`) | $f(x)=\lambda e^{-\lambda x}$ | $\lambda > 0$ | $x \ge 0$ | Durées de vie, temps d'attente |
| **Uniforme continue** (`uniform`) | $f(x)=\frac{1}{b-a}$ | $a < b$ | $x \in [a, b]$ | Génération aléatoire sans a priori |

---

*Références bibliographiques : Casella & Berger (Statistical Inference), Saporta (Probabilités, analyse des données et statistique), Bishop (Pattern Recognition and Machine Learning).*
