from pydantic import BaseModel
from app.models.move import MoveInfo


class BattleStartRequest(BaseModel):
    pokemonName: str
    selectedMoves: list[str]


class BattlePokemon(BaseModel):
    name: str
    types: list[str]
    spriteUrl: str
    currentHp: int
    maxHp: int
    stats: dict[str, int]
    moves: list[MoveInfo]
    statusEffects: list[str] = []


class BattleStartResponse(BaseModel):
    battleId: str
    player: BattlePokemon
    opponent: BattlePokemon


class BattleMoveRequest(BaseModel):
    battleId: str
    moveName: str


class BattleEvent(BaseModel):
    type: str
    actor: str  # "player" | "opponent"
    message: str
    data: dict | None = None


class BattlePokemonState(BaseModel):
    currentHp: int
    maxHp: int
    statusEffects: list[str]
    statModifiers: dict[str, int] = {}


class BattleMoveResponse(BaseModel):
    turnNumber: int
    playerMove: str
    opponentMove: str
    events: list[BattleEvent]
    player: BattlePokemonState
    opponent: BattlePokemonState
    battleOver: bool
    winner: str | None = None


class SideAnalytics(BaseModel):
    pokemonName: str
    totalDamageDealt: int = 0
    totalDamageTaken: int = 0
    movesUsed: dict[str, int] = {}
    superEffectiveHits: int = 0
    notVeryEffectiveHits: int = 0
    criticalHits: int = 0
    statusesInflicted: list[str] = []
    missCount: int = 0


class TurnAnalytics(BaseModel):
    turnNumber: int
    playerMove: str
    opponentMove: str
    playerDamageDealt: int = 0
    opponentDamageDealt: int = 0
    playerHpAfter: int = 0
    opponentHpAfter: int = 0


class BattleAnalytics(BaseModel):
    battleId: str
    totalTurns: int
    winner: str | None = None
    playerAnalytics: SideAnalytics
    opponentAnalytics: SideAnalytics
    turnLog: list[TurnAnalytics] = []
