import React, { useEffect, useRef } from 'react';

export default function PlotlyChart({ data, layout = {}, config = {}, style = {} }) {
  const containerRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current) return;

    let mounted = true;

    const renderChart = () => {
      if (window.Plotly && containerRef.current && mounted) {
        const fullLayout = {
          autosize: true,
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'rgba(10, 14, 23, 0.5)',
          font: { family: 'Outfit, sans-serif', color: '#f8fafc' },
          grid: { color: 'rgba(255, 255, 255, 0.06)' },
          xaxis: { gridcolor: 'rgba(255, 255, 255, 0.06)', zerolinecolor: 'rgba(255, 255, 255, 0.15)' },
          yaxis: { gridcolor: 'rgba(255, 255, 255, 0.06)', zerolinecolor: 'rgba(255, 255, 255, 0.15)' },
          margin: { l: 50, r: 30, t: 50, b: 50 },
          ...layout,
        };

        const fullConfig = {
          responsive: true,
          displayModeBar: true,
          displaylogo: false,
          modeBarButtonsToRemove: ['lasso2d', 'select2d'],
          ...config,
        };

        window.Plotly.newPlot(containerRef.current, data || [], fullLayout, fullConfig);
      }
    };

    if (window.Plotly) {
      renderChart();
    } else {
      // Poll briefly if script is still loading
      const interval = setInterval(() => {
        if (window.Plotly) {
          clearInterval(interval);
          renderChart();
        }
      }, 100);
      return () => clearInterval(interval);
    }

    const handleResize = () => {
      if (window.Plotly && containerRef.current) {
        window.Plotly.Plots.resize(containerRef.current);
      }
    };

    window.addEventListener('resize', handleResize);
    return () => {
      mounted = false;
      window.removeEventListener('resize', handleResize);
      if (window.Plotly && containerRef.current) {
        try {
          window.Plotly.purge(containerRef.current);
        } catch (_) {}
      }
    };
  }, [data, layout, config]);

  return (
    <div
      ref={containerRef}
      style={{
        width: '100%',
        height: '420px',
        ...style,
      }}
    />
  );
}
