import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import type { SideAnalytics } from '../../api/types';

const COLORS = ['#4caf50', '#888', '#ff9800', '#666'];

interface Props {
  player: SideAnalytics;
  opponent: SideAnalytics;
}

function makeData(side: SideAnalytics) {
  const total = side.superEffectiveHits + side.notVeryEffectiveHits + side.missCount;
  const neutralHits = Math.max(0, Object.values(side.movesUsed).reduce((a, b) => a + b, 0) - total);
  return [
    { name: 'Super Effective', value: side.superEffectiveHits },
    { name: 'Neutral', value: neutralHits },
    { name: 'Not Very Effective', value: side.notVeryEffectiveHits },
    { name: 'Missed', value: side.missCount },
  ].filter((d) => d.value > 0);
}

function MiniPie({ data, title }: { data: ReturnType<typeof makeData>; title: string }) {
  return (
    <div style={{ flex: 1 }}>
      <h4 style={{ textAlign: 'center', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>
        {title}
      </h4>
      <ResponsiveContainer width="100%" height={200}>
        <PieChart>
          <Pie data={data} cx="50%" cy="50%" outerRadius={70} dataKey="value" label>
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{ background: '#1a1a2e', border: '1px solid #2a2a4a', borderRadius: '8px' }}
          />
          <Legend wrapperStyle={{ fontSize: '0.7rem' }} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default function EffectivenessChart({ player, opponent }: Props) {
  return (
    <div style={{
      background: 'var(--bg-surface)',
      border: '1px solid var(--border)',
      borderRadius: '12px',
      padding: '1.2rem',
    }}>
      <h3 style={{ fontSize: '0.9rem', fontWeight: 600, marginBottom: '1rem' }}>
        Move Effectiveness
      </h3>
      <div style={{ display: 'flex', gap: '1rem' }}>
        <MiniPie data={makeData(player)} title={player.pokemonName} />
        <MiniPie data={makeData(opponent)} title={opponent.pokemonName} />
      </div>
    </div>
  );
}
