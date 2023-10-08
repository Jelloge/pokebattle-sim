"""Damage calculation — ported from move.py with bug fixes."""

import random

from app.core.type_chart import TYPE_ADVANTAGE, get_type_multiplier, get_effectiveness_label


def calc_damage(
    attacker_level: int,
    attacker_attack: int,
    attacker_sp_attack: int,
    attacker_speed: int,
    attacker_types: list[str],
    attacker_accuracy: float,
    defender_defense: int,
    defender_sp_defense: int,
    defender_types: list[str],
    defender_evasion: float,
    move_power: int,
    move_type: str,
    move_category: str,
    move_accuracy: float,
    move_effects: dict,
) -> dict:
    """Calculate damage for a single hit.

    Returns a dict with keys:
        damage (int), hit (bool), critical (bool),
        effectiveness (str), type_multiplier (float),
        events (list[dict])
    """
    events: list[dict] = []

    # Status moves deal no damage
    if move_category == "Status":
        return {
            "damage": 0,
            "hit": True,
            "critical": False,
            "effectiveness": "normal",
            "type_multiplier": 1.0,
            "events": events,
        }

    # Select attack/defense stats based on category
    if move_category == "Physical":
        a = attacker_attack
        d = defender_defense
    else:
        a = attacker_sp_attack
        d = defender_sp_defense

    # Accuracy check
    hit_check = move_accuracy * attacker_accuracy / defender_evasion
    if random.random() > hit_check:
        events.append({
            "type": "miss",
            "message": "It missed!",
        })
        # Crash damage for moves with Crash effect
        crash_damage = 0
        if "Crash" in move_effects:
            crash_damage = 1
            events.append({
                "type": "recoil",
                "message": "Took 1 HP of crash damage!",
                "data": {"damage": 1},
            })
        return {
            "damage": 0,
            "hit": False,
            "critical": False,
            "effectiveness": "normal",
            "type_multiplier": 1.0,
            "crash_damage": crash_damage,
            "events": events,
        }

    # Critical hit check
    crit_check = random.randint(0, 255)
    crit = 1
    if "HighCrit" in move_effects:
        crit_check = crit_check // 8
    if crit_check < attacker_speed // 2:
        crit = 2
        events.append({
            "type": "critical",
            "message": "A critical hit!",
        })

    # Core damage formula
    damage = ((2 * attacker_level * crit / 5 + 2) * move_power * a / d) / 50 + 2

    # STAB
    if move_type in attacker_types:
        damage *= 1.5

    # Type effectiveness
    type_mult = get_type_multiplier(move_type, defender_types)
    damage *= type_mult

    # Random variance (single roll — fixed double-random bug from original)
    damage *= random.randint(217, 255) / 255
    damage = max(int(damage), 0)

    effectiveness = get_effectiveness_label(type_mult)
    if type_mult == 0:
        events.append({
            "type": "effectiveness",
            "message": "It has no effect...",
            "data": {"effectiveness": "immune", "type_multiplier": type_mult},
        })
    elif type_mult > 1:
        events.append({
            "type": "effectiveness",
            "message": "It's super effective!",
            "data": {"effectiveness": "super", "type_multiplier": type_mult},
        })
    elif type_mult < 1:
        events.append({
            "type": "effectiveness",
            "message": "It's not very effective...",
            "data": {"effectiveness": "not_very", "type_multiplier": type_mult},
        })

    events.append({
        "type": "damage",
        "message": f"{damage} damage dealt!",
        "data": {"damage": damage},
    })

    return {
        "damage": damage,
        "hit": True,
        "critical": crit == 2,
        "effectiveness": effectiveness,
        "type_multiplier": type_mult,
        "events": events,
    }
