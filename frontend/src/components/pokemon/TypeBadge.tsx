import { getTypeColor } from '../../utils/typeColors';

export default function TypeBadge({ type }: { type: string }) {
  return (
    <span style={{
      display: 'inline-block',
      padding: '2px 10px',
      borderRadius: '12px',
      fontSize: '0.7rem',
      fontWeight: 700,
      color: '#fff',
      background: getTypeColor(type),
      textTransform: 'uppercase',
      letterSpacing: '0.5px',
    }}>
      {type}
    </span>
  );
}
