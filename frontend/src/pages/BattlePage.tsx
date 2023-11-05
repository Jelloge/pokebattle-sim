import { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useBattle } from '../hooks/useBattle';
import BattleScene from '../components/battle/BattleScene';
import MovePanel from '../components/battle/MovePanel';
import BattleLog from '../components/battle/BattleLog';
import WinOverlay from '../components/battle/WinOverlay';

export default function BattlePage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { state, loadFromState, playTurn } = useBattle();

  const locationState = location.state as {
    battleId?: string;
    player?: any;
    opponent?: any;
  } | null;

  useEffect(() => {
    if (locationState?.battleId && locationState?.player && locationState?.opponent && !state.battleId) {
      loadFromState(locationState.battleId, locationState.player, locationState.opponent);
    }
  }, []);

  // If no battle data, redirect to selection
  if (!locationState?.player && !state.player) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem' }}>
        <div className="pixel-font" style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', marginBottom: '1rem' }}>
          No battle in progress
        </div>
        <button
          onClick={() => navigate('/')}
          style={{
            padding: '10px 24px',
            borderRadius: '10px',
            background: 'var(--accent)',
            color: '#fff',
            fontWeight: 600,
          }}
        >
          Choose a Pokemon
        </button>
      </div>
    );
  }

  const player = state.player || locationState?.player;
  const opponent = state.opponent || locationState?.opponent;
  const battleId = state.battleId || locationState?.battleId || '';
  const isAnimating = state.animationPhase === 'animating';

  return (
    <div>
      <div style={{ display: 'flex', gap: '1.5rem' }}>
        {/* Left: Battle arena + moves */}
        <div style={{ flex: 3 }}>
          {player && opponent && (
            <BattleScene
              player={player}
              opponent={opponent}
              playerAnimation={state.playerAnimation}
              opponentAnimation={state.opponentAnimation}
            />
          )}
          <div style={{ marginTop: '1rem' }}>
            {player && (
              <MovePanel
                moves={player.moves}
                disabled={isAnimating || state.battleOver}
                onSelectMove={playTurn}
                pokemonName={player.name}
              />
            )}
          </div>
        </div>

        {/* Right: Battle log */}
        <div style={{ flex: 2, minWidth: '280px' }}>
          <h3 className="pixel-font" style={{
            fontSize: '0.7rem',
            color: 'var(--text-secondary)',
            marginBottom: '8px',
          }}>
            Battle Log
          </h3>
          <BattleLog events={state.events} />

          {/* Stats section */}
          {player && opponent && (
            <div style={{
              marginTop: '1rem',
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '0.5rem',
            }}>
              <StatBox label={player.name} stats={player.stats} />
              <StatBox label={opponent.name} stats={opponent.stats} />
            </div>
          )}
        </div>
      </div>

      {state.battleOver && state.winner && player && opponent && (
        <WinOverlay
          winner={state.winner}
          playerName={player.name}
          opponentName={opponent.name}
          battleId={battleId}
        />
      )}
    </div>
  );
}

function StatBox({ label, stats }: { label: string; stats: Record<string, number> }) {
  return (
    <div style={{
      background: 'var(--bg-surface)',
      border: '1px solid var(--border)',
      borderRadius: '8px',
      padding: '8px 10px',
      fontSize: '0.7rem',
    }}>
      <div style={{ fontWeight: 700, marginBottom: '4px', fontSize: '0.75rem' }}>{label}</div>
      {Object.entries(stats).map(([key, val]) => (
        <div key={key} style={{
          display: 'flex',
          justifyContent: 'space-between',
          color: 'var(--text-secondary)',
          lineHeight: '1.6',
        }}>
          <span>{key}</span>
          <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{val}</span>
        </div>
      ))}
    </div>
  );
}
