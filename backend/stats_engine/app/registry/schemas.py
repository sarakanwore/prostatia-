from pydantic import BaseModel, Field
from typing import List, Dict

class MethodParameter(BaseModel):
    type: str = Field(..., description="Le type de la donnée (ex: array<float>, string, int)")
    description: str = Field(..., description="Description humaine du paramètre")

class MethodAssumption(BaseModel):
    id: str = Field(..., description="Identifiant unique de l'hypothèse (ex: normality)")
    name: str = Field(..., description="Nom lisible (ex: Normalité)")
    test_method: str = Field(..., description="Nom de la méthode utilisée pour vérifier cette hypothèse (ex: shapiro_wilk)")
    description: str = Field(..., description="Description de l'hypothèse et pourquoi elle est nécessaire")

class MethodFallback(BaseModel):
    failed_assumption: str = Field(..., description="L'identifiant de l'hypothèse qui a échoué")
    fallback_method: str = Field(..., description="Identifiant de la méthode alternative à utiliser")

class MethodOutput(BaseModel):
    type: str = Field(..., description="Le type de sortie (ex: float, tuple<float, float>)")
    description: str = Field(..., description="Description de la valeur de sortie")

class MethodFiche(BaseModel):
    id: str = Field(..., description="Identifiant unique de la méthode (ex: t_test_independent)")
    name: str = Field(..., description="Nom public de la méthode")
    category: str = Field(..., description="Catégorie (ex: hypothesis_testing, descriptive_stats, regression)")
    description: str = Field(..., description="Description détaillée de l'utilité de cette méthode")
    
    inputs: Dict[str, MethodParameter] = Field(..., description="Dictionnaire des paramètres d'entrée")
    assumptions: List[MethodAssumption] = Field(default_factory=list, description="Liste des conditions d'application")
    fallback_if_assumptions_fail: List[MethodFallback] = Field(default_factory=list, description="Règles de bascule conditionnelles")
    
    outputs: Dict[str, MethodOutput] = Field(..., description="Dictionnaire des résultats de sortie")
    
    numerical_method: str = Field(..., description="Chemin qualifié de la fonction Python/SciPy qui exécute le calcul (ex: scipy.stats.ttest_ind)")
    
    limitations: List[str] = Field(default_factory=list, description="Limites scientifiques de la méthode")
    references: List[str] = Field(default_factory=list, description="Bibliographie ou sources de référence")

