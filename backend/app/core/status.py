"""Status effect application — ported from move.py check_status with bug fixes."""

import random


def apply_status_effects(
    move_effects: dict,
    move_name: str,
    attacker_name: str,
    attacker_types: list[str],
    attacker_start_status: dict,
    attacker_end_status: dict,
    defender_name: str,
    defender_types: list[str],
    defender_start_status: dict,
    defender_end_status: dict,
) -> list[dict]:
    """Check and apply status effects from a move.

    Returns a list of BattleEvent dicts.
    """
    events: list[dict] = []

    # Burn
    if "Burn" in move_effects and "chance" in move_effects["Burn"]:
        # Fire moves thaw frozen targets (fixed: was deleting from wrong dict)
        if "Freeze" in defender_start_status:
            del defender_start_status["Freeze"]
            events.append({
                "type": "status_effect",
                "message": f"{defender_name} thawed out!",
                "data": {"statusEffect": "Freeze"},
            })
        if random.random() < move_effects["Burn"]["chance"]:
            if "Fire" in defender_types:
                events.append({
                    "type": "message",
                    "message": f"{defender_name} is immune to burns!",
                })
            elif "Burn" in defender_start_status:
                events.append({
                    "type": "message",
                    "message": f"{defender_name} is already burned!",
                })
            else:
                defender_start_status["Burn"] = {}
                defender_end_status["Burn"] = {}
                events.append({
                    "type": "status_inflict",
                    "message": f"{defender_name} was burned!",
                    "data": {"statusEffect": "BRN"},
                })

    # Poison
    if "Poison" in move_effects and "chance" in move_effects["Poison"]:
        if random.random() < move_effects["Poison"]["chance"]:
            if "Poison" in defender_end_status:
                events.append({
                    "type": "message",
                    "message": f"{defender_name} is already poisoned!",
                })
            else:
                defender_end_status["Poison"] = {}
                events.append({
                    "type": "status_inflict",
                    "message": f"{defender_name} was poisoned!",
                    "data": {"statusEffect": "PSN"},
                })

    # Freeze
    if "Freeze" in move_effects and "chance" in move_effects["Freeze"]:
        if random.random() < move_effects["Freeze"]["chance"]:
            if "Freeze" in defender_start_status:
                events.append({
                    "type": "message",
                    "message": f"{defender_name} is already frozen!",
                })
            else:
                defender_start_status["Freeze"] = {}
                events.append({
                    "type": "status_inflict",
                    "message": f"{defender_name} was frozen solid!",
                    "data": {"statusEffect": "FRZ"},
                })

    # Paralyze
    if "Paralyze" in move_effects:
        pe = move_effects["Paralyze"]
        immune = "immune" in pe and pe["immune"] in defender_types
        if immune:
            events.append({
                "type": "message",
                "message": f"{defender_name} is immune to paralysis!",
            })
        elif "chance" not in pe or random.random() < pe["chance"]:
            if "Paralyze" in defender_start_status:
                events.append({
                    "type": "message",
                    "message": f"{defender_name} is already paralyzed!",
                })
            else:
                defender_start_status["Paralyze"] = {}
                defender_end_status["Paralyze"] = {}
                events.append({
                    "type": "status_inflict",
                    "message": f"{defender_name} is paralyzed!",
                    "data": {"statusEffect": "PAR"},
                })

    # Flinch
    if "Flinch" in move_effects and "chance" in move_effects["Flinch"]:
        if random.random() < move_effects["Flinch"]["chance"]:
            defender_start_status["Flinch"] = {}
            events.append({
                "type": "status_inflict",
                "message": f"{defender_name} flinched!",
                "data": {"statusEffect": "FLINCH"},
            })

    # Confuse
    if "Confuse" in move_effects:
        ce = move_effects["Confuse"]
        if "chance" not in ce or random.random() < ce["chance"]:
            if "Confuse" in defender_start_status:
                events.append({
                    "type": "message",
                    "message": f"{defender_name} is already confused!",
                })
            else:
                defender_start_status["Confuse"] = {"turns": random.randint(1, 4)}
                events.append({
                    "type": "status_inflict",
                    "message": f"{defender_name} became confused!",
                    "data": {"statusEffect": "CNF"},
                })

    # Sleep
    if "Sleep" in move_effects:
        target_is_self = move_effects["Sleep"].get("target") == "self"
        user_name = attacker_name if target_is_self else defender_name
        user_status = attacker_start_status if target_is_self else defender_start_status
        if "Sleep" in user_status:
            events.append({
                "type": "message",
                "message": f"{user_name} is already asleep!",
            })
        else:
            turns = 2 if move_name == "Rest" else random.randint(1, 5)
            user_status["Sleep"] = {"turns": turns}
            events.append({
                "type": "status_inflict",
                "message": f"{user_name} fell asleep!",
                "data": {"statusEffect": "SLP"},
            })

    # Stat changes
    if "StatChange" in move_effects:
        sc = move_effects["StatChange"]
        if len(sc) > 0 and "target" in sc:
            if random.random() < sc.get("chance", 1.0):
                target_is_user = sc["target"] == "user"
                user_name = attacker_name if target_is_user else defender_name
                user_start = attacker_start_status if target_is_user else defender_start_status
                user_end = attacker_end_status if target_is_user else defender_end_status

                stat_names = [sc["stat"]] if sc.get("stat") != "special" else ["spattack", "spdefense"]
                for stat in stat_names:
                    if "StatChange" not in user_start:
                        user_start["StatChange"] = {}
                        user_end["StatChange"] = {}
                    current = user_start["StatChange"].get(stat, 0)
                    new_val = max(-6, min(6, current + sc["change"]))
                    user_start["StatChange"][stat] = new_val
                    user_end["StatChange"][stat] = new_val
                    events.append({
                        "type": "stat_change",
                        "message": f"{user_name}'s {stat} {'rose' if sc['change'] > 0 else 'fell'}!",
                        "data": {"statName": stat, "statChange": sc["change"]},
                    })

    return events
