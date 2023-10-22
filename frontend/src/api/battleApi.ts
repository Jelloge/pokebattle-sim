import client from './client';
import type { BattleStartResponse, BattleMoveResponse, BattleAnalytics } from './types';

export async function startBattle(pokemonName: string, selectedMoves: string[]): Promise<BattleStartResponse> {
  const res = await client.post<BattleStartResponse>('/battle/start', {
    pokemonName,
    selectedMoves,
  });
  return res.data;
}

export async function executeMove(battleId: string, moveName: string): Promise<BattleMoveResponse> {
  const res = await client.post<BattleMoveResponse>('/battle/move', {
    battleId,
    moveName,
  });
  return res.data;
}

export async function fetchAnalytics(battleId: string): Promise<BattleAnalytics> {
  const res = await client.get<BattleAnalytics>(`/battle/${battleId}/analytics`);
  return res.data;
}
