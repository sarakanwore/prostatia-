import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { X, ShieldCheck, Mail, Lock, User, AlertCircle, CheckCircle2 } from 'lucide-react';

export default function AuthModal() {
  const { isAuthModalOpen, closeAuthModal, authMode, setAuthMode, login, register } = useAuth();
  const [email, setEmail] = useState('analyste@statia.tg');
  const [password, setPassword] = useState('prostatia2026');
  const [fullName, setFullName] = useState('Analyste UEMOA');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  if (!isAuthModalOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (authMode === 'login') {
        await login(email, password);
      } else {
        await register(email, password, fullName);
      }
      setSuccessMsg('Authentification réussie !');
      setTimeout(() => {
        closeAuthModal();
        setSuccessMsg('');
      }, 500);
    } catch (err) {
      setError(err.message || 'Une erreur est survenue lors de l\'authentification');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      zIndex: 100,
      background: 'rgba(5, 8, 14, 0.8)',
      backdropFilter: 'blur(8px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '16px',
    }}>
      <div className="card" style={{
        width: '100%',
        maxWidth: '440px',
        position: 'relative',
        boxShadow: 'var(--shadow-dropdown)',
        border: '1px solid rgba(255, 255, 255, 0.12)',
      }}>
        {/* Close Button */}
        <button
          onClick={closeAuthModal}
          style={{
            position: 'absolute',
            top: '18px',
            right: '18px',
            background: 'transparent',
            border: 'none',
            color: 'var(--text-muted)',
            cursor: 'pointer',
          }}
        >
          <X size={20} />
        </button>

        {/* Modal Header */}
        <div style={{ textAlign: 'center', marginBottom: '24px' }}>
          <div style={{
            width: '48px',
            height: '48px',
            borderRadius: '16px',
            background: 'linear-gradient(135deg, var(--accent-cyan), var(--accent-blue))',
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: '12px',
            boxShadow: 'var(--glow-cyan)',
          }}>
            <ShieldCheck size={26} color="#050b14" />
          </div>
          <h2 style={{ fontSize: '22px', fontWeight: '700', marginBottom: '6px' }}>
            {authMode === 'login' ? 'Connexion Sécurisée' : 'Créer un Compte Analyste'}
          </h2>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>
            Passerelle API Gateway Rust avec authentification JWT
          </p>
        </div>

        {/* Mode Selector Tabs */}
        <div style={{
          display: 'flex',
          background: 'rgba(255, 255, 255, 0.05)',
          borderRadius: 'var(--radius-md)',
          padding: '4px',
          marginBottom: '20px',
        }}>
          <button
            type="button"
            onClick={() => { setAuthMode('login'); setError(null); }}
            style={{
              flex: 1,
              padding: '8px',
              border: 'none',
              borderRadius: 'var(--radius-sm)',
              background: authMode === 'login' ? 'var(--bg-surface-elevated)' : 'transparent',
              color: authMode === 'login' ? 'var(--text-primary)' : 'var(--text-muted)',
              fontWeight: '600',
              fontSize: '13px',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
            }}
          >
            Se Connecter
          </button>
          <button
            type="button"
            onClick={() => { setAuthMode('register'); setError(null); }}
            style={{
              flex: 1,
              padding: '8px',
              border: 'none',
              borderRadius: 'var(--radius-sm)',
              background: authMode === 'register' ? 'var(--bg-surface-elevated)' : 'transparent',
              color: authMode === 'register' ? 'var(--text-primary)' : 'var(--text-muted)',
              fontWeight: '600',
              fontSize: '13px',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
            }}
          >
            S'Inscrire
          </button>
        </div>

        {/* Demo Credentials Tip */}
        <div style={{
          background: 'rgba(0, 242, 254, 0.08)',
          border: '1px solid rgba(0, 242, 254, 0.2)',
          borderRadius: 'var(--radius-sm)',
          padding: '10px 14px',
          fontSize: '12px',
          color: 'var(--text-secondary)',
          marginBottom: '16px',
          lineHeight: '1.5',
        }}>
          💡 <strong>Compte de test prêt à l'emploi :</strong><br />
          Email : <code style={{ color: 'var(--accent-cyan)' }}>analyste@statia.tg</code><br />
          Mot de passe : <code style={{ color: 'var(--accent-cyan)' }}>prostatia2026</code><br />
          <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
            (Ou cliquez sur <em>S'Inscrire</em> pour créer votre propre compte avec le mot de passe de votre choix).
          </span>
        </div>

        {/* Error Alert */}
        {error && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            padding: '10px 14px',
            borderRadius: 'var(--radius-md)',
            background: 'var(--status-error-bg)',
            border: '1px solid rgba(239, 68, 68, 0.3)',
            color: 'var(--status-error)',
            fontSize: '13px',
            marginBottom: '16px',
          }}>
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        {/* Success Alert */}
        {successMsg && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            padding: '10px 14px',
            borderRadius: 'var(--radius-md)',
            background: 'var(--status-success-bg)',
            border: '1px solid rgba(16, 185, 129, 0.3)',
            color: 'var(--status-success)',
            fontSize: '13px',
            marginBottom: '16px',
          }}>
            <CheckCircle2 size={16} />
            <span>{successMsg}</span>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {authMode === 'register' && (
            <div>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: '600', color: 'var(--text-secondary)', marginBottom: '6px' }}>
                Nom Complet
              </label>
              <div style={{ position: 'relative' }}>
                <input
                  id="auth-name"
                  type="text"
                  required
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="Koffi Mensah"
                  className="input-text"
                  style={{ paddingLeft: '38px' }}
                />
                <User size={16} style={{ position: 'absolute', left: '12px', top: '14px', color: 'var(--text-muted)' }} />
              </div>
            </div>
          )}

          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: '600', color: 'var(--text-secondary)', marginBottom: '6px' }}>
              Adresse Email
            </label>
            <div style={{ position: 'relative' }}>
              <input
                id="auth-email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="analyste@statia.tg"
                className="input-text"
                style={{ paddingLeft: '38px' }}
              />
              <Mail size={16} style={{ position: 'absolute', left: '12px', top: '14px', color: 'var(--text-muted)' }} />
            </div>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: '600', color: 'var(--text-secondary)', marginBottom: '6px' }}>
              Mot de Passe
            </label>
            <div style={{ position: 'relative' }}>
              <input
                id="auth-password"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="input-text"
                style={{ paddingLeft: '38px' }}
              />
              <Lock size={16} style={{ position: 'absolute', left: '12px', top: '14px', color: 'var(--text-muted)' }} />
            </div>
          </div>

          <button
            id="btn-auth-submit"
            type="submit"
            disabled={loading}
            className="btn btn-primary"
            style={{ width: '100%', marginTop: '8px', padding: '12px' }}
          >
            {loading ? 'Authentification...' : (authMode === 'login' ? 'Connexion' : 'Créer mon compte')}
          </button>
        </form>

        <p style={{ textAlign: 'center', fontSize: '12px', color: 'var(--text-muted)', marginTop: '20px' }}>
          Jeton cryptographique sécurisé HMAC-SHA256 • Conforme RGPD
        </p>
      </div>
    </div>
  );
}
