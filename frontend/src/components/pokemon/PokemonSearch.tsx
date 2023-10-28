const TYPES = [
  'Normal', 'Fire', 'Water', 'Grass', 'Electric', 'Ice',
  'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug',
  'Rock', 'Ghost', 'Dragon',
];

interface Props {
  search: string;
  onSearchChange: (v: string) => void;
  typeFilter: string | null;
  onTypeFilterChange: (v: string | null) => void;
}

export default function PokemonSearch({ search, onSearchChange, typeFilter, onTypeFilterChange }: Props) {
  return (
    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap' }}>
      <input
        type="text"
        placeholder="Search Pokemon..."
        value={search}
        onChange={(e) => onSearchChange(e.target.value)}
        style={{
          padding: '8px 14px',
          borderRadius: '8px',
          border: '1px solid var(--border)',
          background: 'var(--bg-surface)',
          color: 'var(--text-primary)',
          fontSize: '0.9rem',
          width: '220px',
          outline: 'none',
        }}
      />
      <select
        value={typeFilter || ''}
        onChange={(e) => onTypeFilterChange(e.target.value || null)}
        style={{
          padding: '8px 14px',
          borderRadius: '8px',
          border: '1px solid var(--border)',
          background: 'var(--bg-surface)',
          color: 'var(--text-primary)',
          fontSize: '0.9rem',
          outline: 'none',
        }}
      >
        <option value="">All Types</option>
        {TYPES.map((t) => (
          <option key={t} value={t}>{t}</option>
        ))}
      </select>
    </div>
  );
}
