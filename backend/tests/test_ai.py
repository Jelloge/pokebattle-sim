"""Tests for AI opponent logic."""

import pytest
from app.services.data_loader import game_data
from app.services.ai_service import select_opponent, select_ai_moves, choose_ai_move
from app.services.battle_service import BattlePokemonRuntime
from app.models.move import MoveInfo


@pytest.fixture(autouse=True)
def load_data():
    if not game_data.pokemon_summaries:
        game_data.load()


def _make_move(name, type_="Normal", cat="Physical", power=40, acc=1.0, effects=None):
    return MoveInfo(name=name, type=type_, category=cat, power=power,
                    accuracy=acc, pp=35, description="test", effects=effects or {})


def _make_poke(name="TestMon", types=None, hp=100, atk=80, def_=80,
               spa=80, spd=80, speed=80, moves=None):
    return BattlePokemonRuntime(
        name=name, types=types or ["Normal"], sprite_url="",
        hp=hp, attack=atk, defense=def_, sp_attack=spa,
        sp_defense=spd, speed=speed,
        moves=moves or [_make_move("Tackle")],
    )


def test_select_opponent_not_self():
    opp = select_opponent("Pikachu", 300)
    assert opp != "Pikachu"


def test_select_ai_moves_returns_max_four():
    moves = select_ai_moves("Charizard", ["Grass"])
    assert len(moves) <= 4
    assert len(moves) >= 1


def test_ai_prefers_super_effective():
    fire_move = _make_move("Flamethrower", "Fire", "Special", 90)
    normal_move = _make_move("Tackle", "Normal", "Physical", 40)

    ai = _make_poke("AI", types=["Fire"], moves=[fire_move, normal_move])
    player = _make_poke("Player", types=["Grass"])

    # Run multiple times — AI should prefer Flamethrower most of the time
    fire_count = 0
    for _ in range(50):
        choice = choose_ai_move(ai, player)
        if choice == "Flamethrower":
            fire_count += 1
    assert fire_count > 30  # Should strongly prefer super-effective move


def test_ai_prefers_ko_move():
    weak_move = _make_move("Scratch", "Normal", "Physical", 20)
    strong_move = _make_move("Slam", "Normal", "Physical", 80)

    ai = _make_poke("AI", atk=150, moves=[weak_move, strong_move])
    player = _make_poke("Player", hp=30)  # Low HP — KO opportunity
    player.current_hp = 30

    strong_count = 0
    for _ in range(50):
        choice = choose_ai_move(ai, player)
        if choice == "Slam":
            strong_count += 1
    assert strong_count > 30
