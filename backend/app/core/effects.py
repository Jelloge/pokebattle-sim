"""Parse move effects from scraped descriptions."""

INFLICT_STATUS = {
    "burn": "Burn",
    "freez": "Freeze",
    "paralyz": "Paralyze",
    "flinch": "Flinch",
    "poisoni": "Poison",
    "confus": "Confuse",
}

BOOLEAN_EFFECTS = {
    "increased critical": "HighCrit",
    "one-hit": "Instakill",
    "wild": "Useless",
    "recoil": "Recoil",
    "crash": "Crash",
    " following turn": "Delayed",
    "whatsoever": "Useless",
}

STAT_NAMES = ["Attack", "Defense", "Special", "Speed", "accuracy", "evasion"]


def parse_effects(description: str) -> dict:
    """Parse move description to extract effects.

    Returns a dictionary of effect_name -> effect_data pairs.
    """
    effects: dict = {}

    if "no secondary effect" in description:
        return effects

    sentences = description.split(".")
    for sent in sentences:
        _parse_status_effects(sent, effects)
        _parse_boolean_effects(sent, effects)
        _parse_multihit(sent, effects)
        _parse_stat_changes(sent, effects)
        _parse_poison(sent, effects)
        _parse_self_destruct(sent, effects)
        _parse_sleep(sent, effects)
        _parse_heal(sent, effects)

    # Handle fatigue override: moves that confuse the user after thrashing
    if "Fatigues" in effects and "Confuse" in effects:
        del effects["Confuse"]

    return effects


def _parse_status_effects(sent: str, effects: dict) -> None:
    for phrase, effect in INFLICT_STATUS.items():
        if phrase in sent:
            if effect not in effects:
                effects[effect] = {}
            if "%" in sent and "chance" not in effects[effect]:
                pct_idx = sent.index("%")
                pct_str = sent[pct_idx - 3:pct_idx].strip()
                try:
                    effects[effect]["chance"] = float(pct_str) / 100
                except ValueError:
                    pass
            if "cannot paralyze" in sent:
                idx = sent.index("cannot paralyze") + 16
                type_end = sent.index("-type") if "-type" in sent else len(sent)
                effects.setdefault("Paralyze", {})["immune"] = sent[idx:type_end]


def _parse_boolean_effects(sent: str, effects: dict) -> None:
    for phrase, effect in BOOLEAN_EFFECTS.items():
        if phrase in sent and effect not in effects:
            effects[effect] = {}


def _parse_multihit(sent: str, effects: dict) -> None:
    if "multi-" in sent or "Multihit" in effects:
        if "Multihit" not in effects:
            effects["Multihit"] = {}
        if "twice" in sent:
            effects["Multihit"]["times"] = "twice"
        elif "2-5" in sent:
            effects["Multihit"]["times"] = "multiple"


def _parse_stat_changes(sent: str, effects: dict) -> None:
    triggers = ("increases", "decreases", "lower", "raise")
    if not any(t in sent for t in triggers):
        return

    if "StatChange" not in effects:
        effects["StatChange"] = {"change": 1, "chance": 1.0}

    sc = effects["StatChange"]
    if "target" in sent or "opponent" in sent:
        sc["target"] = "opponent"
    if "user" in sent:
        sc["target"] = "user"
    if "two" in sent:
        sc["change"] = 2
    if "decreases" in sent or "lowering" in sent:
        sc["change"] = abs(sc["change"]) * -1
    if "lowering" in sent:
        sc["chance"] = 0.33

    for stat_name in STAT_NAMES:
        if stat_name in sent:
            sc["stat"] = stat_name.lower()


def _parse_poison(sent: str, effects: dict) -> None:
    if "poisons" in sent and "Poison" not in effects:
        effects["Poison"] = {"chance": 1.0}


def _parse_self_destruct(sent: str, effects: dict) -> None:
    if "user to faint" in sent and "SelfDestruct" not in effects:
        effects["SelfDestruct"] = {}


def _parse_sleep(sent: str, effects: dict) -> None:
    if "sleep" not in sent or "only" in sent:
        return
    if "Sleep" not in effects:
        effects["Sleep"] = {}
    effects["Sleep"]["target"] = "opponent" if "target" in sent else "self"


def _parse_heal(sent: str, effects: dict) -> None:
    if "restore" not in sent or "once" in sent:
        return
    if "Heal" not in effects:
        effects["Heal"] = {}
    if "target" in sent:
        effects["Heal"]["type"] = "lifesteal"
    elif not effects["Heal"]:
        effects["Heal"]["type"] = "selfheal"
