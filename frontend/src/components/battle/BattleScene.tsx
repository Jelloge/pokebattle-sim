import type { BattlePokemon } from '../../api/types';
import SpriteDisplay from './SpriteDisplay';
import HealthBar from './HealthBar';
import StatusIndicator from './StatusIndicator';
import TypeBadge from '../pokemon/TypeBadge';

interface Props {
  player: BattlePokemon;
  opponent: BattlePokemon;
  playerAnimation: string;
  opponentAnimation: string;
}

export default function BattleScene({ player, opponent, playerAnimation, opponentAnimation }: Props) {
  return (
    <div style={{
      background: 'linear-gradient(135deg, #1a3a1a 0%, #2a5a2a 40%, #3a7a3a 100%)',
      borderRadius: '16px',
      padding: '1.5rem',
      position: 'relative',
      minHeight: '280px',
      border: '3px solid #1a2a1a',
      boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
    }}>
      {/* Opponent (top right) */}
      <div className="slide-in-right" style={{
        display: 'flex',
        justifyContent: 'flex-end',
        alignItems: 'flex-start',
        gap: '1rem',
      }}>
        <div style={{ flex: 1, maxWidth: '220px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px' }}>
            <span style={{ fontWeight: 700, fontSize: '0.9rem' }}>{opponent.name}</span>
            {opponent.types.map((t) => <TypeBadge key={t} type={t} />)}
          </div>
          <HealthBar current={opponent.currentHp} max={opponent.maxHp} label="HP" />
          <StatusIndicator statuses={opponent.statusEffects} />
        </div>
        <SpriteDisplay
          src={opponent.spriteUrl}
          name={opponent.name}
          animationClass={opponentAnimation}
        />
      </div>

      {/* Player (bottom left) */}
      <div className="slide-in-left" style={{
        display: 'flex',
        justifyContent: 'flex-start',
        alignItems: 'flex-end',
        gap: '1rem',
      }}>
        <SpriteDisplay
          src={player.spriteUrl}
          name={player.name}
          animationClass={playerAnimation}
          flipped
        />
        <div style={{ flex: 1, maxWidth: '220px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px' }}>
            <span style={{ fontWeight: 700, fontSize: '0.9rem' }}>{player.name}</span>
            {player.types.map((t) => <TypeBadge key={t} type={t} />)}
          </div>
          <HealthBar current={player.currentHp} max={player.maxHp} label="HP" />
          <StatusIndicator statuses={player.statusEffects} />
        </div>
      </div>
    </div>
  );
}
