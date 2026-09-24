import React, { useState, useRef } from 'react';
import { UploadCloud, FileText, CheckCircle2, AlertCircle, RefreshCw, Zap } from 'lucide-react';
import { api } from '../services/api';

export default function DatasetUploader({ onDatasetLoaded, activeDataset, demoDatasets }) {
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileUpload = async (file) => {
    if (!file) return;
    setError(null);
    setUploading(true);

    try {
      const res = await api.uploadDataset(file);
      if (res.status === 'success' || res.dataset_id) {
        const schema = res.schema || {};
        const newDataset = {
          id: res.dataset_id,
          name: file.name,
          rows: schema.row_count || 0,
          columns: schema.columns || [],
          preview: []
        };

        // Fetch preview
        try {
          const previewRes = await api.getPreview(res.dataset_id, 50);
          newDataset.preview = previewRes.data || [];
        } catch (_) {}

        onDatasetLoaded(newDataset);
      }
    } catch (err) {
      // If backend data_service is offline in local test, parse CSV in browser directly!
      try {
        const text = await file.text();
        const lines = text.trim().split('\n');
        if (lines.length > 0) {
          const headers = lines[0].split(',').map(h => h.trim().replace(/^"|"$/g, ''));
          const previewRows = lines.slice(1, 51).map(line => {
            const vals = line.split(',').map(v => v.trim().replace(/^"|"$/g, ''));
            const row = {};
            headers.forEach((h, idx) => {
              const val = vals[idx];
              const num = parseFloat(val);
              row[h] = !isNaN(num) && isFinite(num) ? num : val;
            });
            return row;
          });

          const cols = headers.map(h => {
            const isNum = previewRows.length > 0 && typeof previewRows[0][h] === 'number';
            return { name: h, data_type: isNum ? 'Float64' : 'Utf8', null_count: 0 };
          });

          const localDataset = {
            id: `local_${Date.now()}`,
            name: file.name,
            rows: lines.length - 1,
            columns: cols,
            preview: previewRows
          };
          onDatasetLoaded(localDataset);
          return;
        }
      } catch (parseErr) {
        setError('Impossible de lire le fichier: ' + err.message);
      }
    } finally {
      setUploading(false);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  };

  return (
    <div className="card" style={{ marginBottom: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
        <div>
          <h3 style={{ fontSize: '16px', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <FileText size={18} color="var(--accent-cyan)" />
            <span>Ingestion des Données & Schéma Polars</span>
          </h3>
          <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
            Parseur ultra-rapide Rust Polars (CSV & Excel XLSX) avec inférence automatique des types
          </p>
        </div>

        {/* Demo Quick Pickers */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Jeux d'essai :</span>
          {demoDatasets.map(d => (
            <button
              key={d.id}
              onClick={() => onDatasetLoaded(d)}
              className="btn btn-secondary"
              style={{
                fontSize: '11px',
                padding: '4px 10px',
                borderColor: activeDataset?.id === d.id ? 'var(--accent-cyan)' : 'var(--border-subtle)',
                background: activeDataset?.id === d.id ? 'rgba(0, 242, 254, 0.1)' : 'var(--bg-surface-elevated)',
              }}
            >
              <Zap size={12} color="var(--accent-cyan)" />
              <span>{d.name.split(' ')[0]}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Drag & Drop Zone */}
      <div
        id="drop-zone"
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        style={{
          border: `2px dashed ${isDragging ? 'var(--accent-cyan)' : 'rgba(255, 255, 255, 0.12)'}`,
          borderRadius: 'var(--radius-md)',
          padding: '28px 20px',
          textAlign: 'center',
          background: isDragging ? 'rgba(0, 242, 254, 0.05)' : 'rgba(10, 14, 23, 0.4)',
          cursor: 'pointer',
          transition: 'all 0.25s ease',
        }}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv,.xlsx,.tsv"
          style={{ display: 'none' }}
          onChange={(e) => {
            if (e.target.files?.length) handleFileUpload(e.target.files[0]);
          }}
        />

        <div style={{
          width: '46px',
          height: '46px',
          borderRadius: '50%',
          background: 'rgba(0, 242, 254, 0.1)',
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          marginBottom: '10px',
          color: 'var(--accent-cyan)',
        }}>
          {uploading ? <RefreshCw size={22} className="animate-spin" /> : <UploadCloud size={24} />}
        </div>

        <p style={{ fontSize: '14px', fontWeight: '600', marginBottom: '4px' }}>
          {uploading ? 'Traitement Polars en cours...' : 'Glissez-déposez un fichier CSV ou Excel (.xlsx)'}
        </p>
        <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
          ou cliquez pour parcourir vos fichiers locaux (jusqu'à 100 000 lignes supportées)
        </p>
      </div>

      {error && (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          marginTop: '12px',
          color: 'var(--status-error)',
          fontSize: '12px',
        }}>
          <AlertCircle size={14} />
          <span>{error}</span>
        </div>
      )}

      {/* Active Dataset Schema Chips */}
      {activeDataset && (
        <div style={{ marginTop: '16px', paddingTop: '16px', borderTop: '1px solid var(--border-subtle)' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <CheckCircle2 size={16} color="var(--status-success)" />
              <span style={{ fontWeight: '600', fontSize: '13px' }}>{activeDataset.name}</span>
              <span className="badge badge-info" style={{ fontSize: '11px' }}>
                {activeDataset.rows} observations
              </span>
              <span className="badge badge-purple" style={{ fontSize: '11px' }}>
                {activeDataset.columns?.length || 0} variables
              </span>
            </div>
          </div>

          {/* Variables Types Badges */}
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {activeDataset.columns?.map(col => (
              <div
                key={col.name}
                style={{
                  background: 'var(--bg-surface-elevated)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '4px 10px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  fontSize: '12px',
                }}
              >
                <span style={{ fontWeight: '500', color: 'var(--text-primary)' }}>{col.name}</span>
                <span style={{
                  fontSize: '10px',
                  fontFamily: 'var(--font-mono)',
                  color: col.data_type.includes('Float') || col.data_type.includes('Int') ? 'var(--accent-cyan)' : 'var(--accent-purple)',
                  background: 'rgba(255, 255, 255, 0.05)',
                  padding: '1px 5px',
                  borderRadius: '3px',
                }}>
                  {col.data_type}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
