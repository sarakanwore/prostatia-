import React, { useState, useEffect } from 'react';
import { Send, Compass, Sparkles, HelpCircle, ArrowRight, CornerDownLeft } from 'lucide-react';
import { api } from '../services/api';

export default function VibePromptBar({ dataset, onExecuteAnalysis, isAnalyzing }) {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [loadingSuggestions, setLoadingSuggestions] = useState(false);

  // Fetch Detective Mode suggestions whenever dataset changes
  useEffect(() => {
    if (!dataset?.id) return;
    let isMounted = true;
    setLoadingSuggestions(true);

    api.getDetectiveSuggestions(dataset.id)
      .then(res => {
        if (isMounted && res.suggestions) {
          setSuggestions(res.suggestions);
        }
      })
      .catch(() => {
        if (isMounted) {
          setSuggestions([
            `Quelle est la tendance centrale et la dispersion des variables ?`,
            `Existe-t-il une corrélation significative entre les colonnes numériques ?`,
            `Projeter les données via une ACP pour visualiser les proximités.`
          ]);
        }
      })
      .finally(() => {
        if (isMounted) setLoadingSuggestions(false);
      });

    return () => { isMounted = false; };
  }, [dataset?.id]);

  const handleSubmit = (e) => {
    e?.preventDefault();
    if (!query.trim() || isAnalyzing) return;
    onExecuteAnalysis(query.trim());
  };

  const handleSuggestionClick = (sug) => {
    setQuery(sug);
    onExecuteAnalysis(sug);
  };

  return (
    <div className="card" style={{
      marginBottom: '28px',
      background: 'linear-gradient(180deg, rgba(21, 29, 48, 0.8) 0%, rgba(14, 19, 31, 0.85) 100%)',
      border: '1px solid rgba(0, 242, 254, 0.25)',
      boxShadow: 'var(--glow-cyan)',
      padding: '24px',
    }}>
      {/* Title & Mode Detective Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div style={{
            width: '28px',
            height: '28px',
            borderRadius: '8px',
            background: 'linear-gradient(135deg, var(--accent-cyan), var(--accent-blue))',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}>
            <Sparkles size={16} color="#050b14" />
          </div>
          <div>
            <h2 style={{ fontSize: '17px', fontWeight: '700', letterSpacing: '-0.3px' }}>
              Vibe Analysis — Exploration en Langage Naturel
            </h2>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              Posez votre question statistique librement : l'IA planifie et SciPy calcule de manière certifiée sans hallucination
            </p>
          </div>
        </div>

        <div className="badge badge-purple" style={{ fontSize: '11px', display: 'flex', alignItems: 'center', gap: '6px' }}>
          <Compass size={13} />
          <span>Mode Détective Actif</span>
        </div>
      </div>

      {/* Main Input Form */}
      <form onSubmit={handleSubmit} style={{ position: 'relative', marginBottom: '16px' }}>
        <input
          id="vibe-prompt-input"
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={dataset ? `Ex: Quelle est la corrélation et l'impact entre ${dataset.columns?.[0]?.name || 'la première colonne'} et ${dataset.columns?.[1]?.name || 'la seconde'} ?` : 'Chargez un jeu de données pour démarrer l\'analyse...'}
          disabled={!dataset || isAnalyzing}
          style={{
            width: '100%',
            height: '56px',
            background: 'rgba(8, 12, 20, 0.9)',
            border: '1px solid rgba(255, 255, 255, 0.15)',
            borderRadius: 'var(--radius-lg)',
            padding: '0 120px 0 20px',
            color: 'var(--text-primary)',
            fontSize: '15px',
            fontFamily: 'var(--font-sans)',
            outline: 'none',
            boxShadow: 'inset 0 2px 4px rgba(0, 0, 0, 0.5)',
            transition: 'all 0.25s ease',
          }}
          onFocus={(e) => e.target.style.borderColor = 'var(--accent-cyan)'}
          onBlur={(e) => e.target.style.borderColor = 'rgba(255, 255, 255, 0.15)'}
        />

        <button
          id="btn-run-analysis"
          type="submit"
          disabled={!query.trim() || isAnalyzing || !dataset}
          className="btn btn-primary"
          style={{
            position: 'absolute',
            right: '8px',
            top: '8px',
            bottom: '8px',
            borderRadius: 'var(--radius-md)',
            padding: '0 20px',
            fontSize: '14px',
          }}
        >
          {isAnalyzing ? (
            <span>Calcul SciPy...</span>
          ) : (
            <>
              <span>Analyser</span>
              <CornerDownLeft size={15} />
            </>
          )}
        </button>
      </form>

      {/* Detective Suggestions Pills */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px' }}>
          <Sparkles size={13} color="var(--accent-cyan)" />
          <span style={{ fontSize: '12px', fontWeight: '600', color: 'var(--text-secondary)' }}>
            Suggestions intelligentes du Détective de données :
          </span>
        </div>

        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
          {suggestions.map((sug, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleSuggestionClick(sug)}
              disabled={isAnalyzing}
              style={{
                background: 'rgba(255, 255, 255, 0.04)',
                border: '1px solid rgba(255, 255, 255, 0.08)',
                borderRadius: '9999px',
                padding: '6px 14px',
                fontSize: '12px',
                color: 'var(--text-secondary)',
                cursor: 'pointer',
                textAlign: 'left',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                transition: 'all 0.2s ease',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'rgba(0, 242, 254, 0.1)';
                e.currentTarget.style.borderColor = 'var(--accent-cyan)';
                e.currentTarget.style.color = '#fff';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'rgba(255, 255, 255, 0.04)';
                e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.08)';
                e.currentTarget.style.color = 'var(--text-secondary)';
              }}
            >
              <span>{sug}</span>
              <ArrowRight size={12} color="var(--accent-cyan)" />
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
