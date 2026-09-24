from typing import List, Dict, Any, Optional, Literal, Union
from pydantic import BaseModel, Field

FormatType = Literal["plotly", "vega_lite"]
ChartType = Literal["histogram", "boxplot", "scatter", "correlation_heatmap", "bar", "line", "residuals"]

class HistogramRequest(BaseModel):
    values: List[float] = Field(..., description="Liste des valeurs numériques à analyser")
    title: Optional[str] = Field("Distribution des valeurs", description="Titre du graphique")
    x_label: Optional[str] = Field("Valeur", description="Étiquette de l'axe X")
    nbins: Optional[int] = Field(None, description="Nombre de classes souhaité")
    show_kde: Optional[bool] = Field(True, description="Afficher l'estimation par noyau de densité")
    format: FormatType = Field("plotly", description="Format de restitution")

class BoxplotRequest(BaseModel):
    # Supporte soit un groupe unique via 'values', soit des groupes comparés via 'groups'
    values: Optional[List[float]] = Field(None, description="Valeurs pour un groupe unique")
    groups: Optional[Dict[str, List[float]]] = Field(None, description="Dictionnaire nom_du_groupe -> liste de valeurs")
    title: Optional[str] = Field("Boîte à moustaches", description="Titre du graphique")
    y_label: Optional[str] = Field("Valeur", description="Étiquette de l'axe Y")
    format: FormatType = Field("plotly", description="Format de restitution")

class ScatterRequest(BaseModel):
    x: List[float] = Field(..., description="Coordonnées X")
    y: List[float] = Field(..., description="Coordonnées Y")
    title: Optional[str] = Field("Nuage de points", description="Titre du graphique")
    x_label: Optional[str] = Field("X", description="Étiquette de l'axe X")
    y_label: Optional[str] = Field("Y", description="Étiquette de l'axe Y")
    show_trendline: Optional[bool] = Field(True, description="Calculer et tracer la droite de tendance OLS")
    format: FormatType = Field("plotly", description="Format de restitution")

class CorrelationHeatmapRequest(BaseModel):
    matrix: List[List[float]] = Field(..., description="Matrice de corrélation carrée NxN")
    labels: List[str] = Field(..., description="Noms des variables (longueur N)")
    title: Optional[str] = Field("Matrice de corrélation", description="Titre du graphique")
    format: FormatType = Field("plotly", description="Format de restitution")

class BarChartRequest(BaseModel):
    categories: List[str] = Field(..., description="Noms des catégories")
    values: List[float] = Field(..., description="Valeurs numériques associées")
    title: Optional[str] = Field("Diagramme en barres", description="Titre du graphique")
    x_label: Optional[str] = Field("Catégorie", description="Étiquette de l'axe X")
    y_label: Optional[str] = Field("Valeur", description="Étiquette de l'axe Y")
    format: FormatType = Field("plotly", description="Format de restitution")

class LineChartRequest(BaseModel):
    x: List[Union[float, str]] = Field(..., description="Points de l'axe temporel ou d'abscisse")
    y: List[float] = Field(..., description="Valeurs numériques de la série")
    title: Optional[str] = Field("Évolution temporelle", description="Titre du graphique")
    x_label: Optional[str] = Field("Temps", description="Étiquette de l'axe X")
    y_label: Optional[str] = Field("Valeur", description="Étiquette de l'axe Y")
    format: FormatType = Field("plotly", description="Format de restitution")

class ResidualsRequest(BaseModel):
    predictions: List[float] = Field(..., description="Valeurs prédites (y_pred)")
    residuals: List[float] = Field(..., description="Résidus (y_reel - y_pred)")
    title: Optional[str] = Field("Diagnostic des résidus vs prédictions", description="Titre du graphique")
    format: FormatType = Field("plotly", description="Format de restitution")

class GenericChartRequest(BaseModel):
    chart_type: ChartType = Field(..., description="Type de graphique demandé")
    format: FormatType = Field("plotly", description="Format de sortie (plotly ou vega_lite)")
    data: Dict[str, Any] = Field(..., description="Données d'entrée adaptées au type de graphique")
    config: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Paramètres d'affichage optionnels")

class ChartResponse(BaseModel):
    chart_type: str
    format: str
    spec: Dict[str, Any]
    status: str = "success"
