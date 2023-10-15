from fastapi import APIRouter, HTTPException
from app.models.battle import (
    BattleStartRequest, BattleStartResponse, BattlePokemon,
    BattleMoveRequest, BattleMoveResponse,
)
from app.models.move import MoveInfo
from app.services.data_loader import game_data
from app.services.battle_service import BattleManager, create_battle_pokemon
from app.services.ai_service import select_opponent, select_ai_moves, choose_ai_move
from app.services.analytics_service import AnalyticsTracker

router = APIRouter(prefix="/api/battle", tags=["battle"])

# In-memory battle storage
active_battles: dict[str, BattleManager] = {}
active_analytics: dict[str, AnalyticsTracker] = {}


def _poke_to_response(poke, moves: list[MoveInfo]) -> BattlePokemon:
    return BattlePokemon(
        name=poke.name,
        types=poke.types,
        spriteUrl=poke.sprite_url,
        currentHp=poke.current_hp,
        maxHp=poke.max_hp,
        stats={
            "attack": poke.attack,
            "defense": poke.defense,
            "spAttack": poke.sp_attack,
            "spDefense": poke.sp_defense,
            "speed": poke.speed,
        },
        moves=moves,
        statusEffects=[],
    )


@router.post("/start", response_model=BattleStartResponse)
def start_battle(req: BattleStartRequest):
    if req.pokemonName not in game_data.pokemon_details:
        raise HTTPException(status_code=404, detail=f"Pokemon '{req.pokemonName}' not found")

    # Create player Pokemon
    player = create_battle_pokemon(req.pokemonName, req.selectedMoves)

    # Select and create opponent
    player_raw = game_data.pokemon_raw[req.pokemonName]
    opp_name = select_opponent(req.pokemonName, player_raw["statTotal"])
    opp_moves = select_ai_moves(opp_name, player_raw["types"])
    opponent = create_battle_pokemon(opp_name, opp_moves)

    # Create battle manager
    battle = BattleManager(player, opponent)
    active_battles[battle.battle_id] = battle

    # Create analytics tracker
    tracker = AnalyticsTracker(battle.battle_id, player.name, opponent.name)
    active_analytics[battle.battle_id] = tracker

    return BattleStartResponse(
        battleId=battle.battle_id,
        player=_poke_to_response(player, player.moves),
        opponent=_poke_to_response(opponent, opponent.moves),
    )


@router.post("/move", response_model=BattleMoveResponse)
def execute_move(req: BattleMoveRequest):
    battle = active_battles.get(req.battleId)
    if not battle:
        raise HTTPException(status_code=404, detail="Battle not found")
    if battle.battle_over:
        raise HTTPException(status_code=400, detail="Battle is already over")

    # AI chooses move
    ai_move = choose_ai_move(battle.opponent, battle.player)

    # Execute the turn
    result = battle.execute_turn(req.moveName, ai_move)

    # Record analytics
    tracker = active_analytics.get(req.battleId)
    if tracker:
        tracker.record_turn(result, battle.player.max_hp, battle.opponent.max_hp)

    # Clean up finished battles after a while (keep for analytics)
    return result
