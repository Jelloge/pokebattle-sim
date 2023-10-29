const STATUS_COLORS: Record<string, string> = {
  BRN: '#F08030',
  PSN: '#A040A0',
  PAR: '#F8D030',
  SLP: '#888',
  FRZ: '#98D8D8',
  CNF: '#F85888',
};

export default function StatusIndicator({ statuses }: { statuses: string[] }) {
  if (statuses.length === 0) return null;

  return (
    <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
      {statuses.map((s) => (
        <span
          key={s}
          className="pulse"
          style={{
            display: 'inline-block',
            padding: '1px 8px',
            borderRadius: '4px',
            fontSize: '0.65rem',
            fontWeight: 700,
            color: '#fff',
            background: STATUS_COLORS[s] || '#666',
            letterSpacing: '1px',
          }}
        >
          {s}
        </span>
      ))}
    </div>
  );
}
