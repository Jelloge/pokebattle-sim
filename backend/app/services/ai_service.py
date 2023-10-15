"""AI opponent logic with weighted scoring for move selection."""

import random
import copy
from app.core.damage import calc_damage
from app.core.type_chart import STAT_STAGES
from app.models.move import MoveInfo
from app.services.battle_service import BattlePokemonRuntime
from app.services.data_loader import game_data


def select_opponent(player_name: str, player_stat_total: int) -> str:
    """Select an opponent Pokemon with similar stat total (within ±50)."""
    candidates = []
    for name, raw in game_data.pokemon_raw.items():
        if name == player_name:
            continue
        if abs(raw["statTotal"] - player_stat_total) < 50:
            candidates.append(name)
    if not candidates:
        # Fallback to any Pokemon
        candidates = [n for n in game_data.pokemon_raw if n != player_name]
    return random.choice(candidates)


def select_ai_moves(opponent_name: str, player_types: list[str]) -> list[str]:
    """Select 4 moves for the AI opponent, preferring type-effective ones."""
    raw = game_data.pokemon_raw[opponent_name]
    available = raw["moveset"]

    if len(available) <= 4:
        return available

    scored: list[tuple[str, float]] = []
    for move_name in available:
        key = move_name.lower()
        if key not in game_data.moves:
            continue
        move = game_data.moves[key]
        score = _score_move_for_selection(move, raw, player_types)
        scored.append((move_name, score))

    scored.sort(key=lambda x: x[1], reverse=True)

    # Pick top 3 damage moves + 1 status/utility if available
    damage_picks = []
    status_picks = []
    for name, sc in scored:
        if game_data.moves[name.lower()].category == "Status":
            status_picks.append(name)
        else:
            damage_picks.append(name)

    chosen = damage_picks[:3]
    if status_picks:
        chosen.append(status_picks[0])
    elif len(damage_picks) > 3:
        chosen.append(damage_picks[3])

    return chosen[:4] if chosen else available[:4]


def _score_move_for_selection(move: MoveInfo, attacker_raw: dict,
                              defender_types: list[str]) -> float:
    """Score a move for initial selection."""
    if move.category == "Status":
        return 15.0  # Status moves get a moderate base score

    # Estimate damage
    from app.core.type_chart import get_type_multiplier
    type_mult = get_type_multiplier(move.type, defender_types)
    stab = 1.5 if move.type in attacker_raw["types"] else 1.0
    score = move.power * move.accuracy * type_mult * stab

    if "HighCrit" in move.effects:
        score *= 1.15

    return score


def choose_ai_move(
    ai_poke: BattlePokemonRuntime,
    player_poke: BattlePokemonRuntime,
) -> str:
    """Choose the best move for the AI using weighted scoring."""
    best_score = -999.0
    best_move = ai_poke.moves[0].name

    for move in ai_poke.moves:
        score = _score_move_in_battle(move, ai_poke, player_poke)
        if score > best_score:
            best_score = score
            best_move = move.name

    return best_move


def _score_move_in_battle(
    move: MoveInfo,
    ai: BattlePokemonRuntime,
    player: BattlePokemonRuntime,
) -> float:
    """Score a move based on current battle state."""
    score = 0.0

    ai_hp_pct = ai.current_hp / ai.max_hp
    player_hp_pct = player.current_hp / player.max_hp

    # === Damage score (0-100) ===
    if move.category != "Status" and move.power > 0:
        atk_stages = ai.start_status.get("StatChange", {})
        def_stages = player.start_status.get("StatChange", {})
        eff_attack = int(ai.attack * STAT_STAGES.get(atk_stages.get("attack", 0), 1.0))
        eff_sp_attack = int(ai.sp_attack * STAT_STAGES.get(atk_stages.get("spattack", 0), 1.0))
        eff_defense = int(player.defense * STAT_STAGES.get(def_stages.get("defense", 0), 1.0))
        eff_sp_defense = int(player.sp_defense * STAT_STAGES.get(def_stages.get("spdefense", 0), 1.0))

        result = calc_damage(
            attacker_level=50,
            attacker_attack=eff_attack,
            attacker_sp_attack=eff_sp_attack,
            attacker_speed=ai.speed,
            attacker_types=ai.types,
            attacker_accuracy=ai.accuracy,
            defender_defense=eff_defense,
            defender_sp_defense=eff_sp_defense,
            defender_types=player.types,
            defender_evasion=player.evasion,
            move_power=move.power,
            move_type=move.type,
            move_category=move.category,
            move_accuracy=move.accuracy,
            move_effects=move.effects,
        )
        dmg = result["damage"]
        damage_score = min((dmg / max(player.current_hp, 1)) * 100, 100)

        # KO bonus
        if dmg >= player.current_hp:
            damage_score += 50

        score += damage_score
    elif move.category == "Status":
        score += 10  # Base value for status moves

    # === Status score (0-40) ===
    has_status = bool(player.get_status_labels())
    status_effects = ["Burn", "Freeze", "Paralyze", "Poison", "Sleep", "Confuse"]
    for effect in status_effects:
        if effect in move.effects and not has_status:
            chance = move.effects[effect].get("chance", 1.0)
            score += 30 * chance

            # Strategic bonuses
            if effect == "Paralyze" and ai.speed < player.speed:
                score += 10
            elif effect == "Burn" and player.attack > player.sp_attack:
                score += 10
            elif effect == "Sleep":
                score += 10
            break

    # === Healing score (0-35) ===
    if "Heal" in move.effects and ai_hp_pct < 0.5:
        score += (1 - ai_hp_pct) * 35

    # === Context bonuses ===
    if ai_hp_pct < 0.25:
        if move.category != "Status" and move.power > 0:
            score += 20
        if "Recoil" in move.effects:
            score -= 30

    if player_hp_pct < 0.25:
        if move.category != "Status" and move.power > 0:
            score += 15

    # === Noise for variety ===
    score += random.uniform(-5, 5)

    return score
