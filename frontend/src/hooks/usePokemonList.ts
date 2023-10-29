import { useState, useEffect, useMemo } from 'react';
import { fetchPokemonList } from '../api/pokemonApi';
import type { PokemonSummary } from '../api/types';

export function usePokemonList() {
  const [pokemon, setPokemon] = useState<PokemonSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const [typeFilter, setTypeFilter] = useState<string | null>(null);

  useEffect(() => {
    fetchPokemonList()
      .then(setPokemon)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const filtered = useMemo(() => {
    return pokemon.filter((p) => {
      const matchesSearch = p.name.toLowerCase().includes(search.toLowerCase());
      const matchesType = !typeFilter || p.types.includes(typeFilter);
      return matchesSearch && matchesType;
    });
  }, [pokemon, search, typeFilter]);

  return { pokemon: filtered, loading, error, search, setSearch, typeFilter, setTypeFilter };
}
