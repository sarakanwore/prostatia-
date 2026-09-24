import React, { useEffect, useRef, useState } from 'react';
import { MapPin, Globe, Layers, Info } from 'lucide-react';
import L from 'leaflet';
import { api } from '../services/api';

// Center coordinates for Togo and UEMOA
const MAP_CENTERS = {
  TGO: { center: [8.6195, 1.1], zoom: 7 },
  UEMOA: { center: [12.5, -2.5], zoom: 5 },
};

export default function GeoMap({ zone = 'TGO', data = {}, title = 'Cartographie Thématique' }) {
  const mapContainerRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const geoLayerRef = useRef(null);
  const [activeZone, setActiveZone] = useState(zone);
  const [selectedFeature, setSelectedFeature] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setActiveZone(zone);
  }, [zone]);

  useEffect(() => {
    if (!mapContainerRef.current) return;

    // Initialize Leaflet map if not created
    if (!mapInstanceRef.current) {
      const config = MAP_CENTERS[activeZone] || MAP_CENTERS.TGO;
      const map = L.map(mapContainerRef.current, {
        center: config.center,
        zoom: config.zoom,
        zoomControl: false,
        attributionControl: false,
      });

      L.control.zoom({ position: 'bottomright' }).addTo(map);

      // Dark theme cartographic tiles
      L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 18,
      }).addTo(map);

      mapInstanceRef.current = map;
    }

    const map = mapInstanceRef.current;
    const config = MAP_CENTERS[activeZone] || MAP_CENTERS.TGO;
    map.setView(config.center, config.zoom);

    // Fetch GeoJSON boundaries from geo_service
    setLoading(true);
    api.getBoundaries(activeZone)
      .then(res => {
        if (!res.geojson) return;
        if (geoLayerRef.current) {
          map.removeLayer(geoLayerRef.current);
        }

        const geojson = res.geojson;

        const layer = L.geoJSON(geojson, {
          style: (feature) => {
            const name = feature.properties?.name || feature.properties?.code;
            const val = data[name] || feature.properties?.value;
            // Color based on value or default gradient
            const color = val > 50 ? '#00f2fe' : (val > 30 ? '#4facfe' : '#8b5cf6');
            return {
              fillColor: color,
              weight: 2,
              opacity: 0.9,
              color: '#ffffff',
              dashArray: '3',
              fillOpacity: 0.6,
            };
          },
          onEachFeature: (feature, l) => {
            const props = feature.properties || {};
            const name = props.name || props.code || 'Zone';
            l.on({
              mouseover: (e) => {
                const target = e.target;
                target.setStyle({
                  weight: 3,
                  color: '#00f2fe',
                  fillOpacity: 0.85,
                });
                setSelectedFeature({
                  name,
                  code: props.code,
                  capital: props.capital,
                  population: props.population,
                  value: data[name] || props.value || 'N/A'
                });
              },
              mouseout: (e) => {
                layer.resetStyle(e.target);
              },
              click: () => {
                setSelectedFeature({
                  name,
                  code: props.code,
                  capital: props.capital,
                  population: props.population,
                  value: data[name] || props.value || 'N/A'
                });
              }
            });
          }
        }).addTo(map);

        geoLayerRef.current = layer;
      })
      .catch((err) => {
        console.warn('Geo service unavailable, map offline:', err);
      })
      .finally(() => {
        setLoading(false);
      });

  }, [activeZone, data]);

  return (
    <div style={{ position: 'relative', width: '100%', height: '420px', borderRadius: 'var(--radius-md)', overflow: 'hidden', border: '1px solid var(--border-subtle)' }}>
      {/* Map Element */}
      <div ref={mapContainerRef} style={{ width: '100%', height: '100%' }} />

      {/* Top Controls Overlay */}
      <div style={{
        position: 'absolute',
        top: '12px',
        left: '12px',
        zIndex: 400,
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
      }}>
        <div style={{
          background: 'rgba(10, 14, 23, 0.85)',
          backdropFilter: 'blur(10px)',
          padding: '6px 12px',
          borderRadius: 'var(--radius-sm)',
          border: '1px solid var(--border-subtle)',
          fontSize: '12px',
          fontWeight: '600',
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
        }}>
          <MapPin size={14} color="var(--accent-cyan)" />
          <span>{title}</span>
        </div>

        {/* Zone switcher */}
        <div style={{
          background: 'rgba(10, 14, 23, 0.85)',
          backdropFilter: 'blur(10px)',
          borderRadius: 'var(--radius-sm)',
          padding: '2px',
          border: '1px solid var(--border-subtle)',
          display: 'flex',
          gap: '2px',
        }}>
          <button
            type="button"
            onClick={() => setActiveZone('TGO')}
            style={{
              padding: '4px 10px',
              border: 'none',
              borderRadius: 'var(--radius-sm)',
              fontSize: '11px',
              fontWeight: '600',
              cursor: 'pointer',
              background: activeZone === 'TGO' ? 'var(--accent-cyan)' : 'transparent',
              color: activeZone === 'TGO' ? '#050b14' : 'var(--text-muted)',
            }}
          >
            Togo (5 Régions)
          </button>
          <button
            type="button"
            onClick={() => setActiveZone('UEMOA')}
            style={{
              padding: '4px 10px',
              border: 'none',
              borderRadius: 'var(--radius-sm)',
              fontSize: '11px',
              fontWeight: '600',
              cursor: 'pointer',
              background: activeZone === 'UEMOA' ? 'var(--accent-cyan)' : 'transparent',
              color: activeZone === 'UEMOA' ? '#050b14' : 'var(--text-muted)',
            }}
          >
            UEMOA (8 Pays)
          </button>
        </div>
      </div>

      {/* Selected Feature Info Panel */}
      {selectedFeature && (
        <div style={{
          position: 'absolute',
          bottom: '12px',
          left: '12px',
          zIndex: 400,
          background: 'rgba(10, 14, 23, 0.9)',
          backdropFilter: 'blur(12px)',
          padding: '12px 16px',
          borderRadius: 'var(--radius-md)',
          border: '1px solid rgba(0, 242, 254, 0.3)',
          boxShadow: 'var(--glow-cyan)',
          maxWidth: '280px',
          fontSize: '12px',
        }}>
          <div style={{ fontWeight: '700', fontSize: '14px', color: 'var(--accent-cyan)', marginBottom: '4px' }}>
            {selectedFeature.name}
          </div>
          {selectedFeature.capital && (
            <div style={{ color: 'var(--text-muted)' }}>Chef-lieu : {selectedFeature.capital}</div>
          )}
          {selectedFeature.population && (
            <div style={{ color: 'var(--text-secondary)' }}>
              Population : {typeof selectedFeature.population === 'number' ? selectedFeature.population.toLocaleString('fr-FR') : selectedFeature.population} hab.
            </div>
          )}
          <div style={{ marginTop: '6px', paddingTop: '6px', borderTop: '1px solid rgba(255, 255, 255, 0.08)', fontWeight: '600', color: 'var(--accent-blue)' }}>
            Indicateur territorial : {selectedFeature.value}
          </div>
        </div>
      )}
    </div>
  );
}
