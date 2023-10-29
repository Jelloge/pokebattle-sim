interface Props {
  current: number;
  max: number;
  label: string;
}

export default function HealthBar({ current, max, label }: Props) {
  const pct = Math.max(0, Math.min(100, (current / max) * 100));
  const color = pct > 50 ? '#4caf50' : pct > 20 ? '#ff9800' : '#f44336';

  return (
    <div style={{ width: '100%' }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        fontSize: '0.75rem',
        marginBottom: '3px',
        fontWeight: 600,
      }}>
        <span>{label}</span>
        <span>{Math.max(current, 0)} / {max}</span>
      </div>
      <div style={{
        width: '100%',
        height: '12px',
        background: '#2a2a4a',
        borderRadius: '6px',
        overflow: 'hidden',
        border: '1px solid #3a3a5a',
      }}>
        <div style={{
          width: `${pct}%`,
          height: '100%',
          background: color,
          borderRadius: '6px',
          transition: 'width 0.8s ease-out, background-color 0.3s',
        }} />
      </div>
    </div>
  );
}
