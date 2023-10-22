import client from './client';
import type { PokemonSummary, PokemonDetail, MoveInfo } from './types';

export async function fetchPokemonList(): Promise<PokemonSummary[]> {
  const res = await client.get<PokemonSummary[]>('/pokemon');
  return res.data;
}

export async function fetchPokemonDetail(id: number): Promise<PokemonDetail> {
  const res = await client.get<PokemonDetail>(`/pokemon/${id}`);
  return res.data;
}

export async function fetchPokemonMoves(id: number): Promise<MoveInfo[]> {
  const res = await client.get<MoveInfo[]>(`/pokemon/${id}/moves`);
  return res.data;
}
