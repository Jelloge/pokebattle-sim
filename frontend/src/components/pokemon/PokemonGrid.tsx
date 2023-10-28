import type { PokemonSummary } from '../../api/types';
import PokemonCard from './PokemonCard';

interface Props {
  pokemon: PokemonSummary[];
  selectedId: number | null;
  onSelect: (p: PokemonSummary) => void;
}

export default function PokemonGrid({ pokemon, selectedId, onSelect }: Props) {
  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fill, minmax(120px, 1fr))',
      gap: '0.8rem',
      maxHeight: '60vh',
      overflowY: 'auto',
      padding: '4px',
    }}>
      {pokemon.map((p) => (
        <PokemonCard
          key={p.id}
          pokemon={p}
          selected={p.id === selectedId}
          onClick={() => onSelect(p)}
        />
      ))}
    </div>
  );
}
