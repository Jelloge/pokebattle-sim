import { Link, useLocation } from 'react-router-dom';

export default function Header() {
  const location = useLocation();

  const links = [
    { to: '/', label: 'Select Pokemon' },
    { to: '/battle', label: 'Battle' },
    { to: '/analytics', label: 'Analytics' },
  ];

  return (
    <header style={{
      background: 'var(--bg-secondary)',
      borderBottom: '2px solid var(--accent)',
      padding: '0 2rem',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      height: '60px',
    }}>
      <h1 className="pixel-font" style={{
        fontSize: '1rem',
        color: 'var(--accent)',
        letterSpacing: '1px',
      }}>
        PokeBattle Sim
      </h1>
      <nav style={{ display: 'flex', gap: '1.5rem' }}>
        {links.map((l) => (
          <Link
            key={l.to}
            to={l.to}
            style={{
              color: location.pathname === l.to ? 'var(--accent)' : 'var(--text-secondary)',
              fontWeight: location.pathname === l.to ? 700 : 400,
              fontSize: '0.9rem',
              transition: 'color 0.2s',
            }}
          >
            {l.label}
          </Link>
        ))}
      </nav>
    </header>
  );
}
