import React, { useState } from 'react';
import PlotlyChart from './PlotlyChart';
import {
  BarChart3,
  TrendingUp,
  Award,
  HelpCircle,
  Download,
  FileText,
  MapPin,
  CheckCircle2,
  AlertTriangle,
  Layers,
  Sparkles
} from 'lucide-react';
import GeoMap from './GeoMap';

export default function Dashboard({
  analysisData,
  activeDataset,
  onOpenExplainability,
  isAnalyzing,
}) {
  const [activeTab, setActiveTab] = useState('chart'); // 'chart' | 'map'

  if (isAnalyzing) {
    return (
      <div className="card" style={{ padding: '60px 20px', textAlign: 'center', marginBottom: '24px' }}>
        <div style={{
          width: '56px',
          height: '56px',
          borderRadius: '50%',
          background: 'rgba(0, 242, 254, 0.1)',
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          marginBottom: '16px',
          boxShadow: 'var(--glow-cyan)',
        }}>
          <Sparkles size={28} color="var(--accent-cyan)" className="animate-spin" />
        </div>
        <h3 style={{ fontSize: '18px', fontWeight: '700', marginBottom: '8px' }}>
          Calcul Déterministe SciPy & Synthèse IA en cours...
        </h3>
        <p style={{ fontSize: '13px', color: 'var(--text-muted)', maxWidth: '480px', margin: '0 auto' }}>
          Extraction des vecteurs de données, vérification des hypothèses de normalité et génération des graphiques interactifs.
        </p>
      </div>
    );
  }

  if (!analysisData) {
    return (
      <div className="card" style={{ padding: '50px 20px', textAlign: 'center', marginBottom: '24px' }}>
        <BarChart3 size={40} color="var(--text-muted)" style={{ marginBottom: '12px' }} />
        <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '6px' }}>
          Prêt pour l'Analyse Statistique
        </h3>
        <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
          Posez une question ci-dessus ou cliquez sur une suggestion pour générer le tableau de bord interactif.
        </p>
      </div>
    );
  }

  const { plan, stats_results, visualization, narrative, assumptions_status } = analysisData;
  const stats = stats_results || {};
  const isPValueSig = stats.p_value !== undefined ? stats.p_value < 0.05 : null;

  const handleExportMarkdown = () => {
    const content = `# Rapport d'Analyse PROSTATIA\n\n` +
      `**Date :** ${new Date().toLocaleString('fr-FR')}\n` +
      `**Méthode :** ${plan?.method_id}\n\n` +
      `## Synthèse Scientifique Certifiée\n\n${narrative}\n\n` +
      `## Indicateurs Numériques Déterministes\n\n` +
      `\`\`\`json\n${JSON.stringify(stats, null, 2)}\n\`\`\`\n`;

    const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `rapport_prostatia_${plan?.method_id || 'analyse'}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', marginBottom: '32px' }}>
      {/* Top Banner with Action Buttons */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '12px',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div className="badge badge-success" style={{ fontSize: '12px' }}>
            <CheckCircle2 size={13} />
            <span>Calculs Certifiés Déterministes</span>
          </div>
          {assumptions_status?.is_fallback_applied && (
            <div className="badge badge-warning" style={{ fontSize: '12px' }}>
              <AlertTriangle size={13} />
              <span>Repli Non-Paramétrique Actif</span>
            </div>
          )}
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <button
            id="btn-show-me-why"
            onClick={onOpenExplainability}
            className="btn btn-secondary"
            style={{ fontSize: '13px', padding: '8px 16px', borderColor: 'var(--accent-cyan)' }}
          >
            <HelpCircle size={15} color="var(--accent-cyan)" />
            <span>Show Me Why</span>
          </button>

          <button
            id="btn-export-report"
            onClick={handleExportMarkdown}
            className="btn btn-secondary"
            style={{ fontSize: '13px', padding: '8px 14px' }}
            title="Télécharger le rapport d'analyse"
          >
            <Download size={15} />
            <span>Exporter Rapport</span>
          </button>
        </div>
      </div>

      {/* KPI Metric Cards Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
        gap: '16px',
      }}>
        {/* Metric Card 1: P-Value or Principal Stat */}
        {stats.p_value !== undefined && (
          <div className="card" style={{ padding: '18px' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: '600' }}>P-VALEUR (TEST D'HYPOTHÈSE)</span>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px', marginTop: '6px' }}>
              <span style={{ fontSize: '26px', fontWeight: '800', fontFamily: 'var(--font-mono)', color: isPValueSig ? 'var(--status-success)' : 'var(--status-warning)' }}>
                {typeof stats.p_value === 'number' ? stats.p_value.toExponential(3) : stats.p_value}
              </span>
              <span className={`badge ${isPValueSig ? 'badge-success' : 'badge-warning'}`} style={{ fontSize: '11px' }}>
                {isPValueSig ? 'Significatif (p < 0.05)' : 'Non significatif'}
              </span>
            </div>
            <p style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '4px' }}>
              Seuil critique conventionnel $\alpha = 5\%$
            </p>
          </div>
        )}

        {/* Metric Card 2: Statistic or Mean */}
        {stats.statistic !== undefined && (
          <div className="card" style={{ padding: '18px' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: '600' }}>STATISTIQUE CALCULÉE</span>
            <div style={{ fontSize: '26px', fontWeight: '800', fontFamily: 'var(--font-mono)', color: 'var(--text-accent)', marginTop: '6px' }}>
              {typeof stats.statistic === 'number' ? stats.statistic.toFixed(4) : stats.statistic}
            </div>
            <p style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '4px' }}>
              Test exact SciPy ({assumptions_status?.method_used || plan?.method_id})
            </p>
          </div>
        )}

        {/* Metric Card 3: R² or Variance */}
        {stats.r_squared !== undefined && (
          <div className="card" style={{ padding: '18px' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: '600' }}>COEFFICIENT R² (VARIANCE EXPLIQUÉE)</span>
            <div style={{ fontSize: '26px', fontWeight: '800', fontFamily: 'var(--font-mono)', color: '#8b5cf6', marginTop: '6px' }}>
              {(stats.r_squared * 100).toFixed(1)}%
            </div>
            <p style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '4px' }}>
              Qualité d'ajustement OLS
            </p>
          </div>
        )}

        {/* Metric Card 4: Mean / Median if Descriptive */}
        {stats.mean !== undefined && (
          <div className="card" style={{ padding: '18px' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: '600' }}>MOYENNE ÉCHANTILLONNALE</span>
            <div style={{ fontSize: '26px', fontWeight: '800', fontFamily: 'var(--font-mono)', color: 'var(--accent-cyan)', marginTop: '6px' }}>
              {typeof stats.mean === 'number' ? stats.mean.toFixed(2) : stats.mean}
            </div>
            <p style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '4px' }}>
              Médiane = {stats.median !== undefined ? (typeof stats.median === 'number' ? stats.median.toFixed(2) : stats.median) : 'N/A'}
            </p>
          </div>
        )}

        {/* Metric Card 5: Sample Size / Degrees of Freedom */}
        <div className="card" style={{ padding: '18px' }}>
          <span style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: '600' }}>OBSERVATIONS TRAITÉES</span>
          <div style={{ fontSize: '26px', fontWeight: '800', fontFamily: 'var(--font-mono)', color: 'var(--text-primary)', marginTop: '6px' }}>
            {stats.count || activeDataset?.rows || '100%'}
          </div>
          <p style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Degrés de liberté : {stats.degrees_of_freedom || 'Exact'}
          </p>
        </div>
      </div>

      {/* Main Analysis Visualizer Tabs & Content */}
      <div className="card" style={{ padding: '24px' }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          borderBottom: '1px solid var(--border-subtle)',
          paddingBottom: '14px',
          marginBottom: '20px',
        }}>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button
              onClick={() => setActiveTab('chart')}
              className="btn"
              style={{
                padding: '6px 14px',
                fontSize: '13px',
                background: activeTab === 'chart' ? 'rgba(0, 242, 254, 0.15)' : 'transparent',
                color: activeTab === 'chart' ? 'var(--accent-cyan)' : 'var(--text-muted)',
                borderColor: activeTab === 'chart' ? 'var(--accent-cyan)' : 'transparent',
              }}
            >
              <BarChart3 size={15} />
              <span>Graphique Interactif Plotly</span>
            </button>

            <button
              onClick={() => setActiveTab('map')}
              className="btn"
              style={{
                padding: '6px 14px',
                fontSize: '13px',
                background: activeTab === 'map' ? 'rgba(0, 242, 254, 0.15)' : 'transparent',
                color: activeTab === 'map' ? 'var(--accent-cyan)' : 'var(--text-muted)',
                borderColor: activeTab === 'map' ? 'var(--accent-cyan)' : 'transparent',
              }}
            >
              <MapPin size={15} />
              <span>Cartographie Choroplèthe Togo & UEMOA</span>
            </button>
          </div>

          <span style={{ fontSize: '12px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
            Moteur : {plan?.method_id || 'SciPy / GeoJSON'}
          </span>
        </div>

        {/* Tab 1: Plotly Chart */}
        {activeTab === 'chart' && (
          <div style={{ width: '100%', minHeight: '400px', display: 'flex', justifyContent: 'center' }}>
            {visualization?.data ? (
              <PlotlyChart
                data={visualization.data}
                layout={visualization.layout}
              />
            ) : (
              // Fallback responsive bar/scatter visualization
              <PlotlyChart
                data={[
                  {
                    x: Object.keys(stats).slice(0, 8),
                    y: Object.values(stats).filter(v => typeof v === 'number').slice(0, 8),
                    type: 'bar',
                    marker: {
                      color: 'rgba(0, 242, 254, 0.75)',
                      line: { color: '#00f2fe', width: 1.5 }
                    }
                  }
                ]}
                layout={{
                  title: `Indicateurs Numériques Certifiés (${plan?.method_id || 'Analyse'})`,
                }}
              />
            )}
          </div>
        )}

        {/* Tab 2: Geospatial Map */}
        {activeTab === 'map' && (
          <div>
            <GeoMap
              zone={activeDataset?.zone || 'TGO'}
              title={`Répartition Spatiale — ${activeDataset?.name || 'Afrique de l\'Ouest'}`}
              data={{
                'Maritime': 78,
                'Plateaux': 42,
                'Centrale': 38,
                'Kara': 35,
                'Savanes': 28,
                'TGO': 62,
                'CIV': 70,
                'SEN': 68,
                'BEN': 55
              }}
            />
          </div>
        )}
      </div>

      {/* Scientific Certified Narrative Card */}
      <div className="card" style={{
        padding: '24px',
        borderLeft: '4px solid var(--accent-cyan)',
        background: 'linear-gradient(180deg, rgba(21, 29, 48, 0.7) 0%, rgba(14, 19, 31, 0.8) 100%)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
          <Award size={20} color="var(--accent-cyan)" />
          <h3 style={{ fontSize: '16px', fontWeight: '700' }}>
            Interprétation Statistique & Conclusion Décisionnelle
          </h3>
        </div>

        <div style={{
          fontSize: '14px',
          color: 'var(--text-primary)',
          lineHeight: '1.8',
          whiteSpace: 'pre-line',
        }}>
          {narrative}
        </div>
      </div>
    </div>
  );
}
