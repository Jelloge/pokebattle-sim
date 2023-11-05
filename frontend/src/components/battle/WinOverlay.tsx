import { useNavigate } from 'react-router-dom';

interface Props {
  winner: string;
  playerName: string;
  opponentName: string;
  battleId: string;
}

export default function WinOverlay({ winner, playerName, opponentName, battleId }: Props) {
  const navigate = useNavigate();
  const isPlayerWin = winner === 'player';

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      background: 'rgba(0,0,0,0.7)',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 100,
      animation: 'overlayFadeIn 0.5s ease-out',
    }}>
      <div style={{
        background: 'var(--bg-secondary)',
        border: `3px solid ${isPlayerWin ? 'var(--success)' : 'var(--danger)'}`,
        borderRadius: '20px',
        padding: '2.5rem 3rem',
        textAlign: 'center',
        animation: 'winTextPop 0.5s ease-out',
        maxWidth: '400px',
      }}>
        <div className="pixel-font" style={{
          fontSize: '1.5rem',
          color: isPlayerWin ? 'var(--success)' : 'var(--danger)',
          marginBottom: '0.5rem',
        }}>
          {isPlayerWin ? 'VICTORY!' : 'DEFEAT!'}
        </div>
        <div style={{ fontSize: '1rem', marginBottom: '1.5rem', color: 'var(--text-secondary)' }}>
          {isPlayerWin
            ? `${playerName} defeated ${opponentName}!`
            : `${opponentName} defeated ${playerName}!`}
        </div>
        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
          <button
            onClick={() => navigate('/')}
            style={{
              padding: '10px 20px',
              borderRadius: '10px',
              background: 'var(--bg-card)',
              color: 'var(--text-primary)',
              fontWeight: 600,
              border: '1px solid var(--border)',
            }}
          >
            New Game
          </button>
          <button
            onClick={() => navigate('/analytics', { state: { battleId } })}
            style={{
              padding: '10px 20px',
              borderRadius: '10px',
              background: 'var(--accent)',
              color: '#fff',
              fontWeight: 600,
            }}
          >
            View Analytics
          </button>
        </div>
      </div>
    </div>
  );
}
