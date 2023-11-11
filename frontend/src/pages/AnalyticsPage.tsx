import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { fetchAnalytics } from '../api/battleApi';
import type { BattleAnalytics } from '../api/types';
import BattleSummary from '../components/analytics/BattleSummary';
import DamageChart from '../components/analytics/DamageChart';
import EffectivenessChart from '../components/analytics/EffectivenessChart';

export default function AnalyticsPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [analytics, setAnalytics] = useState<BattleAnalytics | null>(null);
  const [error, setError] = useState<string | null>(null);

  const battleId = (location.state as { battleId?: string })?.battleId;

  useEffect(() => {
    if (battleId) {
      fetchAnalytics(battleId)
        .then(setAnalytics)
        .catch(() => setError('Failed to load analytics'));
    }
  }, [battleId]);

  if (!battleId) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem' }}>
        <div className="pixel-font" style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', marginBottom: '1rem' }}>
          No battle data available
        </div>
        <button
          onClick={() => navigate('/')}
          style={{
            padding: '10px 24px',
            borderRadius: '10px',
            background: 'var(--accent)',
            color: '#fff',
            fontWeight: 600,
          }}
        >
          Start a Battle
        </button>
      </div>
    );
  }

  if (error) {
    return <div style={{ color: 'var(--danger)', padding: '2rem' }}>{error}</div>;
  }

  if (!analytics) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem' }}>
        <div className="pixel-font" style={{ color: 'var(--accent)', fontSize: '0.8rem' }}>
          Loading analytics...
        </div>
      </div>
    );
  }

  // Estimate max HP from first turn or analytics data
  const playerMaxHp = analytics.turnLog.length > 0
    ? analytics.turnLog[0].playerHpAfter + analytics.turnLog[0].opponentDamageDealt
    : 100;
  const opponentMaxHp = analytics.turnLog.length > 0
    ? analytics.turnLog[0].opponentHpAfter + analytics.turnLog[0].playerDamageDealt
    : 100;

  return (
    <div>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '1.5rem',
      }}>
        <h2 className="pixel-font" style={{ fontSize: '1rem', color: 'var(--accent)' }}>
          Battle Analytics
        </h2>
        <button
          onClick={() => navigate('/')}
          style={{
            padding: '8px 20px',
            borderRadius: '8px',
            background: 'var(--bg-card)',
            color: 'var(--text-primary)',
            fontWeight: 600,
            border: '1px solid var(--border)',
          }}
        >
          New Game
        </button>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        <BattleSummary data={analytics} />
        <DamageChart
          turns={analytics.turnLog}
          playerMaxHp={playerMaxHp}
          opponentMaxHp={opponentMaxHp}
        />
        <EffectivenessChart
          player={analytics.playerAnalytics}
          opponent={analytics.opponentAnalytics}
        />

        {/* Move Usage Table */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '1rem',
        }}>
          <MoveTable title={analytics.playerAnalytics.pokemonName} moves={analytics.playerAnalytics.movesUsed} />
          <MoveTable title={analytics.opponentAnalytics.pokemonName} moves={analytics.opponentAnalytics.movesUsed} />
        </div>
      </div>
    </div>
  );
}

function MoveTable({ title, moves }: { title: string; moves: Record<string, number> }) {
  return (
    <div style={{
      background: 'var(--bg-surface)',
      border: '1px solid var(--border)',
      borderRadius: '12px',
      padding: '1rem',
    }}>
      <h4 style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.5rem' }}>
        {title} — Move Usage
      </h4>
      <table style={{ width: '100%', fontSize: '0.8rem' }}>
        <thead>
          <tr style={{ color: 'var(--text-secondary)' }}>
            <th style={{ textAlign: 'left', paddingBottom: '6px' }}>Move</th>
            <th style={{ textAlign: 'right', paddingBottom: '6px' }}>Uses</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(moves).map(([name, count]) => (
            <tr key={name}>
              <td style={{ padding: '3px 0' }}>{name}</td>
              <td style={{ textAlign: 'right', fontWeight: 600 }}>{count}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
