import type { PokemonSummary } from '../../api/types';
import TypeBadge from './TypeBadge';

interface Props {
  pokemon: PokemonSummary;
  selected: boolean;
  onClick: () => void;
}

export default function PokemonCard({ pokemon, selected, onClick }: Props) {
  return (
    <div
      onClick={onClick}
      style={{
        background: selected ? 'var(--bg-card)' : 'var(--bg-surface)',
        border: selected ? '2px solid var(--accent)' : '2px solid var(--border)',
        borderRadius: '12px',
        padding: '0.8rem',
        cursor: 'pointer',
        transition: 'all 0.2s',
        textAlign: 'center',
        transform: selected ? 'scale(1.02)' : 'scale(1)',
      }}
    >
      <img
        src={pokemon.spriteUrl}
        alt={pokemon.name}
        style={{ width: '64px', height: '64px', imageRendering: 'pixelated' }}
        loading="lazy"
      />
      <div style={{ fontWeight: 600, fontSize: '0.85rem', marginTop: '4px' }}>
        {pokemon.name}
      </div>
      <div style={{ display: 'flex', gap: '4px', justifyContent: 'center', marginTop: '4px' }}>
        {pokemon.types.map((t) => (
          <TypeBadge key={t} type={t} />
        ))}
      </div>
      <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
        BST: {pokemon.statTotal}
      </div>
    </div>
  );
}
