export interface PokemonSummary {
  id: number;
  name: string;
  types: string[];
  spriteUrl: string;
  statTotal: number;
}

export interface PokemonStats {
  hp: number;
  attack: number;
  defense: number;
  spAttack: number;
  spDefense: number;
  speed: number;
}

export interface PokemonDetail {
  id: number;
  name: string;
  types: string[];
  spriteUrl: string;
  stats: PokemonStats;
  moves: string[];
}

export interface MoveInfo {
  name: string;
  type: string;
  category: string;
  power: number;
  accuracy: number;
  pp: number;
  description: string;
  effects: Record<string, unknown>;
}

export interface BattlePokemon {
  name: string;
  types: string[];
  spriteUrl: string;
  currentHp: number;
  maxHp: number;
  stats: Record<string, number>;
  moves: MoveInfo[];
  statusEffects: string[];
}

export interface BattleStartResponse {
  battleId: string;
  player: BattlePokemon;
  opponent: BattlePokemon;
}

export interface BattleEvent {
  type: string;
  actor: string;
  message: string;
  data?: Record<string, unknown>;
}

export interface BattlePokemonState {
  currentHp: number;
  maxHp: number;
  statusEffects: string[];
  statModifiers: Record<string, number>;
}

export interface BattleMoveResponse {
  turnNumber: number;
  playerMove: string;
  opponentMove: string;
  events: BattleEvent[];
  player: BattlePokemonState;
  opponent: BattlePokemonState;
  battleOver: boolean;
  winner: string | null;
}

export interface SideAnalytics {
  pokemonName: string;
  totalDamageDealt: number;
  totalDamageTaken: number;
  movesUsed: Record<string, number>;
  superEffectiveHits: number;
  notVeryEffectiveHits: number;
  criticalHits: number;
  statusesInflicted: string[];
  missCount: number;
}

export interface TurnAnalytics {
  turnNumber: number;
  playerMove: string;
  opponentMove: string;
  playerDamageDealt: number;
  opponentDamageDealt: number;
  playerHpAfter: number;
  opponentHpAfter: number;
}

export interface BattleAnalytics {
  battleId: string;
  totalTurns: number;
  winner: string | null;
  playerAnalytics: SideAnalytics;
  opponentAnalytics: SideAnalytics;
  turnLog: TurnAnalytics[];
}
