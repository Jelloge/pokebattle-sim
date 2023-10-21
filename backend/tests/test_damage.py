"""Tests for damage calculation and type effectiveness."""

import pytest
from app.core.type_chart import get_type_multiplier, get_effectiveness_label
from app.core.stat_calc import calc_hp, calc_stat
from app.core.damage import calc_damage


def test_type_effectiveness_super():
    assert get_type_multiplier("Fire", ["Grass"]) == 2.0


def test_type_effectiveness_not_very():
    assert get_type_multiplier("Fire", ["Water"]) == 0.5


def test_type_effectiveness_immune():
    assert get_type_multiplier("Normal", ["Ghost"]) == 0.0


def test_type_effectiveness_dual_type():
    # Fire vs Grass/Bug = 2 * 2 = 4x
    assert get_type_multiplier("Fire", ["Grass", "Bug"]) == 4.0


def test_effectiveness_label():
    assert get_effectiveness_label(2.0) == "super"
    assert get_effectiveness_label(0.5) == "not_very"
    assert get_effectiveness_label(0.0) == "immune"
    assert get_effectiveness_label(1.0) == "normal"


def test_calc_hp():
    # Bulbasaur base HP 45 at level 50
    assert calc_hp(45, 50) == 105


def test_calc_stat():
    # Bulbasaur base Attack 49 at level 50
    assert calc_stat(49, 50) == 54


def test_damage_status_move():
    result = calc_damage(
        attacker_level=50, attacker_attack=100, attacker_sp_attack=100,
        attacker_speed=80, attacker_types=["Fire"],
        attacker_accuracy=1.0,
        defender_defense=80, defender_sp_defense=80,
        defender_types=["Grass"], defender_evasion=1.0,
        move_power=0, move_type="Fire", move_category="Status",
        move_accuracy=1.0, move_effects={},
    )
    assert result["damage"] == 0
    assert result["hit"] is True


def test_damage_deals_positive():
    result = calc_damage(
        attacker_level=50, attacker_attack=100, attacker_sp_attack=100,
        attacker_speed=80, attacker_types=["Fire"],
        attacker_accuracy=1.0,
        defender_defense=80, defender_sp_defense=80,
        defender_types=["Grass"], defender_evasion=1.0,
        move_power=90, move_type="Fire", move_category="Special",
        move_accuracy=1.0, move_effects={},
    )
    # Super effective + STAB = should deal significant damage
    assert result["damage"] > 0
    assert result["hit"] is True
