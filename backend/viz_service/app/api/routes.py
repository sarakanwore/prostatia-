from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.models.schemas import (
    HistogramRequest,
    BoxplotRequest,
    ScatterRequest,
    CorrelationHeatmapRequest,
    BarChartRequest,
    LineChartRequest,
    ResidualsRequest,
    GenericChartRequest,
    ChartResponse,
)
from app.services import plotly_builder, vegalite_builder

router = APIRouter(prefix="/api/v1/chart", tags=["visualizations"])

@router.post("/histogram", response_model=ChartResponse)
def generate_histogram(req: HistogramRequest):
    try:
        if req.format == "vega_lite":
            spec = vegalite_builder.build_vega_histogram(
                values=req.values,
                title=req.title,
                x_label=req.x_label,
                nbins=req.nbins
            )
        else:
            spec = plotly_builder.build_histogram(
                values=req.values,
                title=req.title,
                x_label=req.x_label,
                nbins=req.nbins,
                show_kde=bool(req.show_kde)
            )
        return ChartResponse(chart_type="histogram", format=req.format, spec=spec)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération de l'histogramme: {str(e)}")

@router.post("/boxplot", response_model=ChartResponse)
def generate_boxplot(req: BoxplotRequest):
    try:
        if req.format == "vega_lite":
            spec = vegalite_builder.build_vega_boxplot(
                values=req.values,
                groups=req.groups,
                title=req.title,
                y_label=req.y_label
            )
        else:
            spec = plotly_builder.build_boxplot(
                values=req.values,
                groups=req.groups,
                title=req.title,
                y_label=req.y_label
            )
        return ChartResponse(chart_type="boxplot", format=req.format, spec=spec)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération du boxplot: {str(e)}")

@router.post("/scatter", response_model=ChartResponse)
def generate_scatter(req: ScatterRequest):
    try:
        if req.format == "vega_lite":
            spec = vegalite_builder.build_vega_scatter(
                x=req.x,
                y=req.y,
                title=req.title,
                x_label=req.x_label,
                y_label=req.y_label
            )
        else:
            spec = plotly_builder.build_scatter(
                x=req.x,
                y=req.y,
                title=req.title,
                x_label=req.x_label,
                y_label=req.y_label,
                show_trendline=bool(req.show_trendline)
            )
        return ChartResponse(chart_type="scatter", format=req.format, spec=spec)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération du scatter: {str(e)}")

@router.post("/correlation_heatmap", response_model=ChartResponse)
def generate_correlation_heatmap(req: CorrelationHeatmapRequest):
    try:
        if req.format == "vega_lite":
            spec = vegalite_builder.build_vega_heatmap(
                matrix=req.matrix,
                labels=req.labels,
                title=req.title
            )
        else:
            spec = plotly_builder.build_correlation_heatmap(
                matrix=req.matrix,
                labels=req.labels,
                title=req.title
            )
        return ChartResponse(chart_type="correlation_heatmap", format=req.format, spec=spec)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération de la heatmap: {str(e)}")

@router.post("/bar", response_model=ChartResponse)
def generate_bar(req: BarChartRequest):
    try:
        if req.format == "vega_lite":
            spec = vegalite_builder.build_vega_bar_chart(
                categories=req.categories,
                values=req.values,
                title=req.title,
                x_label=req.x_label,
                y_label=req.y_label
            )
        else:
            spec = plotly_builder.build_bar_chart(
                categories=req.categories,
                values=req.values,
                title=req.title,
                x_label=req.x_label,
                y_label=req.y_label
            )
        return ChartResponse(chart_type="bar", format=req.format, spec=spec)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération du bar chart: {str(e)}")

@router.post("/line", response_model=ChartResponse)
def generate_line(req: LineChartRequest):
    try:
        if req.format == "vega_lite":
            spec = vegalite_builder.build_vega_line_chart(
                x=req.x,
                y=req.y,
                title=req.title,
                x_label=req.x_label,
                y_label=req.y_label
            )
        else:
            spec = plotly_builder.build_line_chart(
                x=req.x,
                y=req.y,
                title=req.title,
                x_label=req.x_label,
                y_label=req.y_label
            )
        return ChartResponse(chart_type="line", format=req.format, spec=spec)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération de la ligne: {str(e)}")

@router.post("/residuals", response_model=ChartResponse)
def generate_residuals(req: ResidualsRequest):
    try:
        if req.format == "vega_lite":
            spec = vegalite_builder.build_vega_residuals(
                predictions=req.predictions,
                residuals=req.residuals,
                title=req.title
            )
        else:
            spec = plotly_builder.build_residuals(
                predictions=req.predictions,
                residuals=req.residuals,
                title=req.title
            )
        return ChartResponse(chart_type="residuals", format=req.format, spec=spec)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération des résidus: {str(e)}")

@router.post("/generate", response_model=ChartResponse)
def generate_generic(req: GenericChartRequest):
    """
    Point d'entrée unique acceptant un payload dynamique.
    """
    try:
        data = req.data
        cfg = req.config or {}
        chart_type = req.chart_type
        fmt = req.format

        if chart_type == "histogram":
            sub_req = HistogramRequest(
                values=data["values"],
                title=cfg.get("title", "Distribution des valeurs"),
                x_label=cfg.get("x_label", "Valeur"),
                nbins=cfg.get("nbins"),
                show_kde=cfg.get("show_kde", True),
                format=fmt
            )
            return generate_histogram(sub_req)

        elif chart_type == "boxplot":
            sub_req = BoxplotRequest(
                values=data.get("values"),
                groups=data.get("groups"),
                title=cfg.get("title", "Boîte à moustaches"),
                y_label=cfg.get("y_label", "Valeur"),
                format=fmt
            )
            return generate_boxplot(sub_req)

        elif chart_type == "scatter":
            sub_req = ScatterRequest(
                x=data["x"],
                y=data["y"],
                title=cfg.get("title", "Nuage de points"),
                x_label=cfg.get("x_label", "X"),
                y_label=cfg.get("y_label", "Y"),
                show_trendline=cfg.get("show_trendline", True),
                format=fmt
            )
            return generate_scatter(sub_req)

        elif chart_type == "correlation_heatmap":
            sub_req = CorrelationHeatmapRequest(
                matrix=data["matrix"],
                labels=data["labels"],
                title=cfg.get("title", "Matrice de corrélation"),
                format=fmt
            )
            return generate_correlation_heatmap(sub_req)

        elif chart_type == "bar":
            sub_req = BarChartRequest(
                categories=data["categories"],
                values=data["values"],
                title=cfg.get("title", "Diagramme en barres"),
                x_label=cfg.get("x_label", "Catégorie"),
                y_label=cfg.get("y_label", "Valeur"),
                format=fmt
            )
            return generate_bar(sub_req)

        elif chart_type == "line":
            sub_req = LineChartRequest(
                x=data["x"],
                y=data["y"],
                title=cfg.get("title", "Courbe d'évolution"),
                x_label=cfg.get("x_label", "Temps"),
                y_label=cfg.get("y_label", "Valeur"),
                format=fmt
            )
            return generate_line(sub_req)

        elif chart_type == "residuals":
            sub_req = ResidualsRequest(
                predictions=data["predictions"],
                residuals=data["residuals"],
                title=cfg.get("title", "Diagnostic des résidus vs prédictions"),
                format=fmt
            )
            return generate_residuals(sub_req)

        else:
            raise HTTPException(status_code=400, detail=f"Type de graphique non reconnu: {chart_type}")

    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Champ requis manquant dans 'data': {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
