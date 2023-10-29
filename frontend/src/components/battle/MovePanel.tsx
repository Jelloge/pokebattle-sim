import type { MoveInfo } from '../../api/types';
import MoveButton from './MoveButton';

interface Props {
  moves: MoveInfo[];
  disabled: boolean;
  onSelectMove: (name: string) => void;
  pokemonName: string;
}

export default function MovePanel({ moves, disabled, onSelectMove, pokemonName }: Props) {
  return (
    <div>
      <div className="pixel-font" style={{
        fontSize: '0.65rem',
        color: 'var(--text-secondary)',
        marginBottom: '8px',
      }}>
        What will {pokemonName} do?
      </div>
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '8px',
      }}>
        {moves.map((m) => (
          <MoveButton
            key={m.name}
            move={m}
            disabled={disabled}
            onClick={() => onSelectMove(m.name)}
          />
        ))}
      </div>
    </div>
  );
}
