"""Tests for battle service."""

import pytest
from app.services.data_loader import game_data
from app.services.battle_service import BattleManager, BattlePokemonRuntime, create_battle_pokemon
from app.models.move import MoveInfo


@pytest.fixture(autouse=True)
def load_data():
    if not game_data.pokemon_summaries:
        game_data.load()


def _make_move(name="Tackle", type_="Normal", cat="Physical", power=40, acc=1.0):
    return MoveInfo(name=name, type=type_, category=cat, power=power,
                    accuracy=acc, pp=35, description="A basic attack.")


def _make_poke(name="TestMon", types=None, hp=100, atk=80, def_=80,
               spa=80, spd=80, speed=80, moves=None):
    return BattlePokemonRuntime(
        name=name, types=types or ["Normal"], sprite_url="",
        hp=hp, attack=atk, defense=def_, sp_attack=spa,
        sp_defense=spd, speed=speed,
        moves=moves or [_make_move()],
    )


def test_battle_turn_executes():
    p = _make_poke("Player", moves=[_make_move("Tackle")])
    o = _make_poke("Opponent", moves=[_make_move("Scratch")])
    battle = BattleManager(p, o)
    result = battle.execute_turn("Tackle", "Scratch")
    assert result.turnNumber == 1
    assert len(result.events) > 0


def test_battle_ends_on_faint():
    p = _make_poke("Player", hp=200, atk=200, moves=[_make_move("Slam", power=120)])
    o = _make_poke("Opponent", hp=50, def_=20, moves=[_make_move("Tackle")])
    battle = BattleManager(p, o)
    # With 200 attack vs 20 defense and 120 power, should KO in one hit
    result = battle.execute_turn("Slam", "Tackle")
    # Battle should eventually end
    for _ in range(20):
        if battle.battle_over:
            break
        result = battle.execute_turn("Slam", "Tackle")
    assert battle.battle_over


def test_create_battle_pokemon():
    poke = create_battle_pokemon("Charizard", ["Flamethrower", "Slash"])
    assert poke.name == "Charizard"
    assert poke.max_hp > 0
    assert len(poke.moves) > 0


def test_status_effects_list():
    p = _make_poke()
    p.start_status["Burn"] = {}
    p.end_status["Burn"] = {}
    p.start_status["Paralyze"] = {}
    labels = p.get_status_labels()
    assert "BRN" in labels
    assert "PAR" in labels
