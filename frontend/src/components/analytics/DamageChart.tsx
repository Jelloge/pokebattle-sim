import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  BarChart, Bar, Legend,
} from 'recharts';
import { useState } from 'react';
import type { TurnAnalytics } from '../../api/types';

interface Props {
  turns: TurnAnalytics[];
  playerMaxHp: number;
  opponentMaxHp: number;
}

export default function DamageChart({ turns, playerMaxHp, opponentMaxHp }: Props) {
  const [view, setView] = useState<'hp' | 'damage'>('hp');

  const hpData = turns.map((t) => ({
    turn: t.turnNumber,
    Player: Math.round((t.playerHpAfter / playerMaxHp) * 100),
    Opponent: Math.round((t.opponentHpAfter / opponentMaxHp) * 100),
  }));

  const dmgData = turns.map((t) => ({
    turn: t.turnNumber,
    Player: t.playerDamageDealt,
    Opponent: t.opponentDamageDealt,
  }));

  return (
    <div style={{
      background: 'var(--bg-surface)',
      border: '1px solid var(--border)',
      borderRadius: '12px',
      padding: '1.2rem',
    }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '1rem',
      }}>
        <h3 style={{ fontSize: '0.9rem', fontWeight: 600 }}>
          {view === 'hp' ? 'HP Over Time' : 'Damage Per Turn'}
        </h3>
        <div style={{ display: 'flex', gap: '6px' }}>
          {(['hp', 'damage'] as const).map((v) => (
            <button
              key={v}
              onClick={() => setView(v)}
              style={{
                padding: '4px 12px',
                borderRadius: '6px',
                fontSize: '0.75rem',
                background: view === v ? 'var(--accent)' : 'var(--bg-card)',
                color: view === v ? '#fff' : 'var(--text-secondary)',
                border: 'none',
                fontWeight: 600,
              }}
            >
              {v === 'hp' ? 'HP %' : 'Damage'}
            </button>
          ))}
        </div>
      </div>

      <ResponsiveContainer width="100%" height={250}>
        {view === 'hp' ? (
          <AreaChart data={hpData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#2a2a4a" />
            <XAxis dataKey="turn" stroke="#666" fontSize={12} />
            <YAxis stroke="#666" fontSize={12} domain={[0, 100]} />
            <Tooltip
              contentStyle={{ background: '#1a1a2e', border: '1px solid #2a2a4a', borderRadius: '8px' }}
              labelStyle={{ color: '#e0e0e0' }}
            />
            <Area type="monotone" dataKey="Player" stroke="#4caf50" fill="#4caf5040" strokeWidth={2} />
            <Area type="monotone" dataKey="Opponent" stroke="#f44336" fill="#f4433640" strokeWidth={2} />
            <Legend />
          </AreaChart>
        ) : (
          <BarChart data={dmgData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#2a2a4a" />
            <XAxis dataKey="turn" stroke="#666" fontSize={12} />
            <YAxis stroke="#666" fontSize={12} />
            <Tooltip
              contentStyle={{ background: '#1a1a2e', border: '1px solid #2a2a4a', borderRadius: '8px' }}
              labelStyle={{ color: '#e0e0e0' }}
            />
            <Bar dataKey="Player" fill="#4caf50" radius={[4, 4, 0, 0]} />
            <Bar dataKey="Opponent" fill="#f44336" radius={[4, 4, 0, 0]} />
            <Legend />
          </BarChart>
        )}
      </ResponsiveContainer>
    </div>
  );
}
