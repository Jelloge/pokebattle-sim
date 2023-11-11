import type { BattleAnalytics } from '../../api/types';

export default function BattleSummary({ data }: { data: BattleAnalytics }) {
  const cards = [
    { label: 'Total Turns', value: data.totalTurns, color: 'var(--accent)' },
    { label: 'Winner', value: data.winner === 'player' ? data.playerAnalytics.pokemonName : data.opponentAnalytics.pokemonName, color: 'var(--success)' },
    { label: 'Player Damage', value: data.playerAnalytics.totalDamageDealt, color: '#F08030' },
    { label: 'Opponent Damage', value: data.opponentAnalytics.totalDamageDealt, color: '#6890F0' },
  ];

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
      gap: '1rem',
    }}>
      {cards.map((c) => (
        <div key={c.label} style={{
          background: 'var(--bg-surface)',
          border: '1px solid var(--border)',
          borderRadius: '12px',
          padding: '1.2rem',
          textAlign: 'center',
        }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginBottom: '6px' }}>
            {c.label}
          </div>
          <div style={{ fontSize: '1.5rem', fontWeight: 700, color: c.color }}>
            {c.value}
          </div>
        </div>
      ))}
    </div>
  );
}
