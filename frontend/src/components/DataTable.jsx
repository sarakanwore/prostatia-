import React, { useState } from 'react';
import { Table, Sparkles, Filter, ChevronDown, CheckCheck, RefreshCw } from 'lucide-react';
import { api } from '../services/api';

export default function DataTable({ dataset, onDatasetCleaned }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [cleaning, setCleaning] = useState(false);
  const [cleanReport, setCleanReport] = useState(null);

  if (!dataset || !dataset.preview || dataset.preview.length === 0) {
    return null;
  }

  const columns = dataset.columns?.map(c => c.name) || Object.keys(dataset.preview[0] || {});

  const filteredRows = dataset.preview.filter(row => {
    if (!searchTerm) return true;
    return Object.values(row).some(val => 
      String(val).toLowerCase().includes(searchTerm.toLowerCase())
    );
  });

  const handleCleanData = async () => {
    if (!dataset.id || dataset.id.startsWith('local_') || dataset.id.startsWith('demo_')) {
      // Local clean simulation
      setCleaning(true);
      setTimeout(() => {
        setCleaning(false);
        setCleanReport({ cleaned_rows: dataset.rows, nulls_dropped: 0 });
      }, 600);
      return;
    }

    setCleaning(true);
    try {
      const res = await api.cleanDataset(dataset.id);
      setCleanReport(res);
      if (onDatasetCleaned) onDatasetCleaned(res);
    } catch (e) {
      setCleanReport({ error: e.message });
    } finally {
      setCleaning(false);
    }
  };

  return (
    <div className="card" style={{ marginBottom: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Table size={18} color="var(--accent-blue)" />
          <h3 style={{ fontSize: '15px', fontWeight: '700' }}>
            Explorateur de Données Brutes ({filteredRows.length} lignes affichées)
          </h3>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          {/* Search */}
          <div style={{ position: 'relative' }}>
            <input
              type="text"
              placeholder="Filtrer les observations..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input-text"
              style={{
                padding: '6px 12px',
                fontSize: '12px',
                width: '200px',
                height: '34px',
              }}
            />
          </div>

          {/* Clean Data Action */}
          <button
            id="btn-clean-dataset"
            onClick={handleCleanData}
            disabled={cleaning}
            className="btn btn-secondary"
            style={{ padding: '6px 14px', fontSize: '12px', height: '34px' }}
          >
            {cleaning ? (
              <>
                <RefreshCw size={13} className="animate-spin" />
                <span>Nettoyage Polars...</span>
              </>
            ) : (
              <>
                <Sparkles size={13} color="var(--accent-cyan)" />
                <span>Nettoyer (Doublons & Nulls)</span>
              </>
            )}
          </button>
        </div>
      </div>

      {cleanReport && (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '8px 12px',
          borderRadius: 'var(--radius-sm)',
          background: 'var(--status-success-bg)',
          border: '1px solid rgba(16, 185, 129, 0.3)',
          color: 'var(--status-success)',
          fontSize: '12px',
          marginBottom: '12px',
        }}>
          <CheckCheck size={16} />
          <span>
            Jeu nettoyé avec succès : {cleanReport.cleaned_rows} lignes conservées sans valeur manquante.
          </span>
        </div>
      )}

      {/* Table Container */}
      <div style={{
        overflowX: 'auto',
        borderRadius: 'var(--radius-md)',
        border: '1px solid var(--border-subtle)',
        background: 'rgba(9, 13, 21, 0.6)',
        maxHeight: '280px',
      }}>
        <table style={{
          width: '100%',
          borderCollapse: 'collapse',
          fontSize: '13px',
          textAlign: 'left',
          fontFamily: 'var(--font-sans)',
        }}>
          <thead>
            <tr style={{
              background: 'var(--bg-surface-elevated)',
              borderBottom: '1px solid var(--border-subtle)',
              position: 'sticky',
              top: 0,
              zIndex: 2,
            }}>
              <th style={{ padding: '10px 14px', width: '45px', color: 'var(--text-muted)', fontSize: '11px', fontFamily: 'var(--font-mono)' }}>#</th>
              {columns.map(col => (
                <th key={col} style={{ padding: '10px 14px', fontWeight: '600', color: 'var(--text-primary)' }}>
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filteredRows.map((row, idx) => (
              <tr
                key={idx}
                style={{
                  borderBottom: '1px solid rgba(255, 255, 255, 0.04)',
                  transition: 'background 0.15s ease',
                }}
                onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.03)'}
                onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
              >
                <td style={{ padding: '9px 14px', color: 'var(--text-muted)', fontSize: '11px', fontFamily: 'var(--font-mono)' }}>
                  {idx + 1}
                </td>
                {columns.map(col => {
                  const val = row[col];
                  const isNum = typeof val === 'number';
                  return (
                    <td key={col} style={{
                      padding: '9px 14px',
                      color: isNum ? 'var(--text-accent)' : 'var(--text-primary)',
                      fontFamily: isNum ? 'var(--font-mono)' : 'inherit',
                      fontSize: isNum ? '12px' : '13px',
                    }}>
                      {val !== null && val !== undefined ? String(val) : <span style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>null</span>}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
