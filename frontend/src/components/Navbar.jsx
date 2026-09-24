import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Database, Activity, ShieldCheck, User, LogOut, Sparkles, BookOpen, Layers } from 'lucide-react';

export default function Navbar({ activeDataset, onSelectDataset, demoDatasets }) {
  const { user, isAuthenticated, logout, openLoginModal } = useAuth();
  const [gatewayOnline, setGatewayOnline] = useState(true);

  useEffect(() => {
    // Quick ping check
    fetch('http://localhost:8080/health')
      .then(res => setGatewayOnline(res.ok))
      .catch(() => setGatewayOnline(false));
  }, []);

  return (
    <header style={{
      position: 'sticky',
      top: 0,
      zIndex: 50,
      background: 'rgba(10, 14, 23, 0.85)',
      backdropFilter: 'blur(20px)',
      WebkitBackdropFilter: 'blur(20px)',
      borderBottom: '1px solid var(--border-subtle)',
      padding: '0 24px',
      height: '68px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
    }}>
      {/* Brand */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        <div style={{
          width: '40px',
          height: '40px',
          borderRadius: '12px',
          background: 'linear-gradient(135deg, #00f2fe, #4facfe)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: 'var(--glow-cyan)',
        }}>
          <Activity size={22} color="#050b14" strokeWidth={2.5} />
        </div>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{
              fontSize: '19px',
              fontWeight: '800',
              letterSpacing: '-0.5px',
              background: 'linear-gradient(135deg, #ffffff, #94a3b8)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}>
              PROSTATIA
            </span>
            <span className="badge badge-purple" style={{ fontSize: '10px', padding: '2px 7px' }}>
              v1.0 IDE
            </span>
          </div>
          <p style={{ fontSize: '11px', color: 'var(--text-muted)', margin: 0 }}>
            Moteur Statistique Déterministe & IA E2E
          </p>
        </div>
      </div>

      {/* Center Dataset Selector */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          background: 'var(--bg-surface-elevated)',
          padding: '6px 14px',
          borderRadius: 'var(--radius-md)',
          border: '1px solid var(--border-subtle)',
          fontSize: '13px',
        }}>
          <Database size={15} color="var(--accent-cyan)" />
          <span style={{ color: 'var(--text-muted)' }}>Jeu de données :</span>
          <select
            id="dataset-selector"
            value={activeDataset?.id || ''}
            onChange={(e) => {
              const selected = demoDatasets.find(d => d.id === e.target.value);
              if (selected) onSelectDataset(selected);
            }}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--text-primary)',
              fontWeight: '600',
              fontFamily: 'var(--font-sans)',
              outline: 'none',
              cursor: 'pointer',
            }}
          >
            {demoDatasets.map(d => (
              <option key={d.id} value={d.id} style={{ background: '#0e131f', color: '#fff' }}>
                {d.name} ({d.rows} lignes)
              </option>
            ))}
          </select>
        </div>

        {/* Microservices Gateway Status indicator */}
        <div className={`badge ${gatewayOnline ? 'badge-success' : 'badge-warning'}`} style={{ fontSize: '11px' }}>
          <span style={{
            width: '6px',
            height: '6px',
            borderRadius: '50%',
            background: gatewayOnline ? '#10b981' : '#f59e0b',
            boxShadow: gatewayOnline ? '0 0 8px #10b981' : 'none'
          }}></span>
          {gatewayOnline ? 'Gateway :8080 Connecté' : 'Mode Autonome'}
        </div>
      </div>

      {/* Right User Actions */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <a
          href="http://localhost:8000/docs"
          target="_blank"
          rel="noopener noreferrer"
          className="btn btn-ghost"
          style={{ padding: '7px 12px', fontSize: '13px' }}
          title="Consulter le Swagger OpenAPI"
        >
          <BookOpen size={16} />
          <span>API Docs</span>
        </a>

        {isAuthenticated ? (
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '6px 12px',
              borderRadius: 'var(--radius-md)',
              background: 'var(--bg-surface-elevated)',
              border: '1px solid var(--border-subtle)',
              fontSize: '13px'
            }}>
              <User size={15} color="var(--accent-blue)" />
              <span style={{ fontWeight: '500' }}>{user?.email?.split('@')[0]}</span>
            </div>
            <button
              id="btn-logout"
              onClick={logout}
              className="btn btn-ghost"
              style={{ padding: '8px', color: 'var(--status-error)' }}
              title="Déconnexion"
            >
              <LogOut size={16} />
            </button>
          </div>
        ) : (
          <button
            id="btn-login-modal"
            onClick={openLoginModal}
            className="btn btn-primary"
            style={{ padding: '8px 18px', fontSize: '13px' }}
          >
            <ShieldCheck size={16} />
            <span>Connexion JWT</span>
          </button>
        )}
      </div>
    </header>
  );
}
