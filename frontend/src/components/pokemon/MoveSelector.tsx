import type { MoveInfo } from '../../api/types';
import { getTypeColor } from '../../utils/typeColors';

interface Props {
  moves: MoveInfo[];
  selected: string[];
  onToggle: (moveName: string) => void;
}

export default function MoveSelector({ moves, selected, onToggle }: Props) {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      gap: '6px',
      maxHeight: '50vh',
      overflowY: 'auto',
    }}>
      <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '4px' }}>
        Select up to 4 moves ({selected.length}/4)
      </div>
      {moves.map((m) => {
        const isSelected = selected.includes(m.name);
        const disabled = !isSelected && selected.length >= 4;
        return (
          <label
            key={m.name}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '6px 10px',
              borderRadius: '8px',
              background: isSelected ? 'var(--bg-card)' : 'var(--bg-surface)',
              border: isSelected ? '1px solid var(--accent)' : '1px solid var(--border)',
              cursor: disabled ? 'not-allowed' : 'pointer',
              opacity: disabled ? 0.5 : 1,
              transition: 'all 0.15s',
            }}
          >
            <input
              type="checkbox"
              checked={isSelected}
              disabled={disabled}
              onChange={() => onToggle(m.name)}
              style={{ accentColor: 'var(--accent)' }}
            />
            <span style={{
              width: '8px',
              height: '8px',
              borderRadius: '50%',
              background: getTypeColor(m.type),
              flexShrink: 0,
            }} />
            <span style={{ flex: 1, fontSize: '0.8rem', fontWeight: 500 }}>
              {m.name}
            </span>
            <span style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>
              {m.category === 'Status' ? 'Status' : `${m.power} PWR`}
            </span>
          </label>
        );
      })}
    </div>
  );
}
