import { useRef, useEffect } from 'react';
import type { BattleEvent } from '../../api/types';

export default function BattleLog({ events }: { events: BattleEvent[] }) {
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [events.length]);

  return (
    <div style={{
      background: 'var(--bg-surface)',
      border: '1px solid var(--border)',
      borderRadius: '10px',
      padding: '12px',
      height: '250px',
      overflowY: 'auto',
      fontSize: '0.8rem',
      lineHeight: '1.6',
    }}>
      {events.length === 0 && (
        <div style={{ color: 'var(--text-secondary)', fontStyle: 'italic' }}>
          Choose a move to begin the battle...
        </div>
      )}
      {events.map((e, i) => (
        <div
          key={i}
          className="fade-in"
          style={{
            color: e.type === 'damage' ? 'var(--danger)'
              : e.type === 'effectiveness' ? '#F8D030'
              : e.type === 'critical' ? '#FF6B6B'
              : e.type === 'heal' ? 'var(--success)'
              : e.type === 'faint' ? 'var(--accent)'
              : e.type === 'status_inflict' ? '#A040A0'
              : 'var(--text-primary)',
            fontWeight: e.type === 'faint' || e.type === 'critical' ? 700 : 400,
          }}
        >
          {e.message}
        </div>
      ))}
      <div ref={endRef} />
    </div>
  );
}
