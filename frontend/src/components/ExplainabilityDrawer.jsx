import React from 'react';
import { X, ShieldCheck, CheckCircle2, AlertTriangle, BookOpen, Code, Cpu, Award } from 'lucide-react';

export default function ExplainabilityDrawer({ isOpen, onClose, plan, assumptions, statsResults, activeMethodFiche }) {
  if (!isOpen) return null;

  const failed = assumptions?.failed_assumptions || [];
  const methodUsed = assumptions?.method_used || plan?.method_id || 'Moteur SciPy';
  const isFallback = assumptions?.is_fallback_applied || failed.length > 0;

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      zIndex: 150,
      background: 'rgba(5, 8, 14, 0.7)',
      backdropFilter: 'blur(6px)',
      display: 'flex',
      justifyContent: 'flex-end',
      transition: 'opacity 0.3s ease',
    }}>
      <div style={{
        width: '100%',
        maxWidth: '520px',
        height: '100%',
        background: 'var(--bg-surface)',
        borderLeft: '1px solid rgba(255, 255, 255, 0.1)',
        boxShadow: '-10px 0 40px rgba(0, 0, 0, 0.7)',
        display: 'flex',
        flexDirection: 'column',
        overflowY: 'auto',
        padding: '28px',
      }}>
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              width: '36px',
              height: '36px',
              borderRadius: '10px',
              background: 'linear-gradient(135deg, var(--accent-cyan), var(--accent-blue))',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}>
              <ShieldCheck size={20} color="#050b14" />
            </div>
            <div>
              <h2 style={{ fontSize: '18px', fontWeight: '700', letterSpacing: '-0.3px' }}>
                Show Me Why — Traçabilité & Preuve
              </h2>
              <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                Audit scientifique des calculs et conformité méthodologique
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--text-muted)',
              cursor: 'pointer',
              padding: '6px',
              borderRadius: '6px',
            }}
          >
            <X size={20} />
          </button>
        </div>

        {/* Zero Hallucination Guarantee Seal */}
        <div style={{
          background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.12), rgba(0, 242, 254, 0.08))',
          border: '1px solid rgba(16, 185, 129, 0.3)',
          borderRadius: 'var(--radius-md)',
          padding: '16px',
          marginBottom: '20px',
          display: 'flex',
          alignItems: 'flex-start',
          gap: '12px',
        }}>
          <Award size={24} color="var(--status-success)" style={{ flexShrink: 0, marginTop: '2px' }} />
          <div>
            <h4 style={{ fontSize: '14px', fontWeight: '700', color: 'var(--status-success)', marginBottom: '4px' }}>
              Garantie Zéro Hallucination STATIA
            </h4>
            <p style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: '1.5' }}>
              Les calculs statistiques présentés sont 100% déterministes. Le grand modèle de langage (LLM) est strictement cantonné au rôle d'orchestrateur sémantique et de vulgarisateur ; il n'a exécuté aucune opération arithmétique.
            </p>
          </div>
        </div>

        {/* Method Fiche Overview */}
        <div className="card" style={{ padding: '18px', marginBottom: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
            <Cpu size={16} color="var(--accent-cyan)" />
            <h3 style={{ fontSize: '14px', fontWeight: '700' }}>Algorithme Mathématique Exécuté</h3>
          </div>

          <div style={{
            background: 'rgba(0, 0, 0, 0.4)',
            padding: '10px 14px',
            borderRadius: 'var(--radius-sm)',
            fontFamily: 'var(--font-mono)',
            fontSize: '12px',
            color: 'var(--text-accent)',
            marginBottom: '10px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}>
            <span>Fonction :</span>
            <span style={{ fontWeight: '600' }}>{methodUsed}</span>
          </div>

          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: '1.5', marginBottom: '12px' }}>
            {activeMethodFiche?.description || plan?.explanation || "Exécution de la méthode via les routines certifiées SciPy et scikit-learn."}
          </p>

          {activeMethodFiche?.numerical_method && (
            <div style={{ fontSize: '12px', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Code size={13} />
              <span>Routine : <code>{activeMethodFiche.numerical_method}</code></span>
            </div>
          )}
        </div>

        {/* Assumptions Verification Report */}
        <div className="card" style={{ padding: '18px', marginBottom: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
            <h3 style={{ fontSize: '14px', fontWeight: '700' }}>Vérification des Hypothèses Statistiques</h3>
            <span className={`badge ${isFallback ? 'badge-warning' : 'badge-success'}`}>
              {isFallback ? 'Repli Non-Paramétrique Engagé' : 'Hypothèses Vérifiées'}
            </span>
          </div>

          {/* Normality Test Shapiro-Wilk */}
          <div style={{
            padding: '10px 12px',
            borderRadius: 'var(--radius-sm)',
            background: failed.includes('normality') ? 'var(--status-warning-bg)' : 'var(--status-success-bg)',
            border: `1px solid ${failed.includes('normality') ? 'rgba(245, 158, 11, 0.3)' : 'rgba(16, 185, 129, 0.3)'}`,
            marginBottom: '8px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            fontSize: '12px',
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              {failed.includes('normality') ? (
                <AlertTriangle size={15} color="var(--status-warning)" />
              ) : (
                <CheckCircle2 size={15} color="var(--status-success)" />
              )}
              <span style={{ fontWeight: '600' }}>Hypothèse de Normalité (Shapiro-Wilk)</span>
            </div>
            <span style={{ fontFamily: 'var(--font-mono)' }}>
              {failed.includes('normality') ? 'Non respectée (p < 0.05)' : 'Conforme (p ≥ 0.05)'}
            </span>
          </div>

          {/* Homoscedasticity Test Levene */}
          <div style={{
            padding: '10px 12px',
            borderRadius: 'var(--radius-sm)',
            background: failed.includes('homoscedasticity') ? 'var(--status-warning-bg)' : 'var(--status-success-bg)',
            border: `1px solid ${failed.includes('homoscedasticity') ? 'rgba(245, 158, 11, 0.3)' : 'rgba(16, 185, 129, 0.3)'}`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            fontSize: '12px',
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              {failed.includes('homoscedasticity') ? (
                <AlertTriangle size={15} color="var(--status-warning)" />
              ) : (
                <CheckCircle2 size={15} color="var(--status-success)" />
              )}
              <span style={{ fontWeight: '600' }}>Homoscédasticité (Test de Levene)</span>
            </div>
            <span style={{ fontFamily: 'var(--font-mono)' }}>
              {failed.includes('homoscedasticity') ? 'Variances inégales' : 'Variances homogènes'}
            </span>
          </div>
        </div>

        {/* Academic References & Course Material */}
        <div className="card" style={{ padding: '18px', marginTop: 'auto' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
            <BookOpen size={16} color="var(--accent-purple)" />
            <h3 style={{ fontSize: '14px', fontWeight: '700' }}>Références Académiques</h3>
          </div>
          <ul style={{ fontSize: '12px', color: 'var(--text-secondary)', paddingLeft: '18px', lineHeight: '1.6' }}>
            <li>UCAO / Université de Lomé — Cours d'Analyse des données et Statistique Inférentielle (2025-2026).</li>
            <li>Saporta, G. (2011). <em>Probabilités, analyse des données et statistique</em>. Technip.</li>
            <li>Virtanen, P. et al. (2020). <em>SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python</em>. Nature Methods.</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
