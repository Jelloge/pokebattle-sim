import type { MoveInfo } from '../../api/types';
import { getTypeColor } from '../../utils/typeColors';

interface Props {
  move: MoveInfo;
  disabled: boolean;
  onClick: () => void;
}

export default function MoveButton({ move, disabled, onClick }: Props) {
  const bg = getTypeColor(move.type);

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        background: bg,
        color: '#fff',
        padding: '12px 16px',
        borderRadius: '10px',
        fontWeight: 700,
        fontSize: '0.85rem',
        textAlign: 'left',
        transition: 'all 0.15s',
        filter: disabled ? 'grayscale(0.5)' : 'none',
        boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
        display: 'flex',
        flexDirection: 'column',
        gap: '2px',
      }}
    >
      <span>{move.name}</span>
      <span style={{ fontSize: '0.65rem', opacity: 0.8, fontWeight: 400 }}>
        {move.category} {move.power > 0 ? `| ${move.power} PWR` : ''} | {move.pp} PP
      </span>
    </button>
  );
}
