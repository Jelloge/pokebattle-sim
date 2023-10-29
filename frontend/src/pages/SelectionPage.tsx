import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { usePokemonList } from '../hooks/usePokemonList';
import { fetchPokemonMoves } from '../api/pokemonApi';
import { startBattle } from '../api/battleApi';
import type { PokemonSummary, MoveInfo } from '../api/types';
import PokemonGrid from '../components/pokemon/PokemonGrid';
import PokemonSearch from '../components/pokemon/PokemonSearch';
import MoveSelector from '../components/pokemon/MoveSelector';
import TypeBadge from '../components/pokemon/TypeBadge';

export default function SelectionPage() {
  const { pokemon, loading, search, setSearch, typeFilter, setTypeFilter } = usePokemonList();
  const navigate = useNavigate();

  const [selected, setSelected] = useState<PokemonSummary | null>(null);
  const [moves, setMoves] = useState<MoveInfo[]>([]);
  const [selectedMoves, setSelectedMoves] = useState<string[]>([]);
  const [starting, setStarting] = useState(false);

  useEffect(() => {
    if (selected) {
      setSelectedMoves([]);
      fetchPokemonMoves(selected.id).then(setMoves);
    }
  }, [selected]);

  const toggleMove = (name: string) => {
    setSelectedMoves((prev) =>
      prev.includes(name)
        ? prev.filter((m) => m !== name)
        : prev.length < 4 ? [...prev, name] : prev
    );
  };

  const handleStart = async () => {
    if (!selected || selectedMoves.length === 0) return;
    setStarting(true);
    try {
      const res = await startBattle(selected.name, selectedMoves);
      navigate('/battle', { state: { battleId: res.battleId, player: res.player, opponent: res.opponent } });
    } finally {
      setStarting(false);
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem' }}>
        <div className="pixel-font" style={{ color: 'var(--accent)' }}>Loading Pokemon...</div>
      </div>
    );
  }

  return (
    <div>
      <h2 className="pixel-font" style={{ fontSize: '1rem', marginBottom: '1rem', color: 'var(--accent)' }}>
        Choose Your Pokemon
      </h2>

      <div style={{ display: 'flex', gap: '1.5rem' }}>
        {/* Left: Pokemon grid */}
        <div style={{ flex: 2 }}>
          <PokemonSearch
            search={search} onSearchChange={setSearch}
            typeFilter={typeFilter} onTypeFilterChange={setTypeFilter}
          />
          <div style={{ marginTop: '1rem' }}>
            <PokemonGrid pokemon={pokemon} selectedId={selected?.id ?? null} onSelect={setSelected} />
          </div>
        </div>

        {/* Right: Details + Move selection */}
        <div style={{ flex: 1, minWidth: '280px' }}>
          {selected ? (
            <div style={{
              background: 'var(--bg-surface)',
              border: '1px solid var(--border)',
              borderRadius: '12px',
              padding: '1.2rem',
            }}>
              {/* Pokemon info */}
              <div style={{ textAlign: 'center', marginBottom: '1rem' }}>
                <img
                  src={selected.spriteUrl}
                  alt={selected.name}
                  style={{ width: '80px', height: '80px', imageRendering: 'pixelated' }}
                />
                <div style={{ fontWeight: 700, fontSize: '1.1rem', marginTop: '4px' }}>
                  {selected.name}
                </div>
                <div style={{ display: 'flex', gap: '4px', justifyContent: 'center', marginTop: '4px' }}>
                  {selected.types.map((t) => <TypeBadge key={t} type={t} />)}
                </div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
                  Base Stat Total: {selected.statTotal}
                </div>
              </div>

              {/* Move selection */}
              <MoveSelector moves={moves} selected={selectedMoves} onToggle={toggleMove} />

              {/* Start button */}
              <button
                onClick={handleStart}
                disabled={selectedMoves.length === 0 || starting}
                style={{
                  width: '100%',
                  marginTop: '1rem',
                  padding: '12px',
                  borderRadius: '10px',
                  background: selectedMoves.length > 0 ? 'var(--accent)' : 'var(--bg-card)',
                  color: '#fff',
                  fontWeight: 700,
                  fontSize: '0.9rem',
                  transition: 'all 0.2s',
                }}
              >
                {starting ? 'Starting...' : `Battle! (${selectedMoves.length} moves)`}
              </button>
            </div>
          ) : (
            <div style={{
              background: 'var(--bg-surface)',
              border: '1px solid var(--border)',
              borderRadius: '12px',
              padding: '2rem',
              textAlign: 'center',
              color: 'var(--text-secondary)',
            }}>
              Select a Pokemon to see its moves
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
