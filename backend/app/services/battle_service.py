"""Battle state machine — ported from battle.py with all bugs fixed."""

import random
import uuid
import copy
from app.core.damage import calc_damage
from app.core.status import apply_status_effects
from app.core.type_chart import STAT_STAGES
from app.models.battle import (
    BattleEvent, BattlePokemonState, BattleMoveResponse,
)
from app.models.move import MoveInfo
from app.services.data_loader import game_data


class BattlePokemonRuntime:
    """Mutable runtime state for a Pokemon in battle."""

    def __init__(self, name: str, types: list[str], sprite_url: str,
                 hp: int, attack: int, defense: int, sp_attack: int,
                 sp_defense: int, speed: int, moves: list[MoveInfo]) -> None:
        self.name = name
        self.types = types
        self.sprite_url = sprite_url
        self.max_hp = hp
        self.current_hp = hp
        self.base_attack = attack
        self.base_defense = defense
        self.base_sp_attack = sp_attack
        self.base_sp_defense = sp_defense
        self.base_speed = speed
        # Current (modified) stats
        self.attack = attack
        self.defense = defense
        self.sp_attack = sp_attack
        self.sp_defense = sp_defense
        self.speed = speed
        self.accuracy = 1.0
        self.evasion = 1.0
        self.moves = moves
        self.start_status: dict = {}
        self.end_status: dict = {}

    def get_status_labels(self) -> list[str]:
        labels = []
        if "Burn" in self.start_status:
            labels.append("BRN")
        if "Poison" in self.end_status:
            labels.append("PSN")
        if "Paralyze" in self.start_status:
            labels.append("PAR")
        if "Sleep" in self.start_status:
            labels.append("SLP")
        if "Freeze" in self.start_status:
            labels.append("FRZ")
        if "Confuse" in self.start_status:
            labels.append("CNF")
        return labels

    def get_stat_modifiers(self) -> dict[str, int]:
        return dict(self.start_status.get("StatChange", {}))

    def to_state(self) -> BattlePokemonState:
        return BattlePokemonState(
            currentHp=max(self.current_hp, 0),
            maxHp=self.max_hp,
            statusEffects=self.get_status_labels(),
            statModifiers=self.get_stat_modifiers(),
        )


class BattleManager:
    """Manages the state of a single battle."""

    def __init__(self, player: BattlePokemonRuntime, opponent: BattlePokemonRuntime) -> None:
        self.battle_id = str(uuid.uuid4())
        self.player = player
        self.opponent = opponent
        self.turn_number = 0
        self.battle_over = False
        self.winner: str | None = None

    def execute_turn(self, player_move_name: str, opponent_move_name: str) -> BattleMoveResponse:
        self.turn_number += 1
        events: list[BattleEvent] = []

        player_move = self._find_move(self.player, player_move_name)
        opponent_move = self._find_move(self.opponent, opponent_move_name)

        # Determine turn order by speed (paralysis halves speed)
        p_speed = self.player.speed
        o_speed = self.opponent.speed
        if "Paralyze" in self.player.start_status:
            p_speed = p_speed // 2
        if "Paralyze" in self.opponent.start_status:
            o_speed = o_speed // 2

        if p_speed >= o_speed:
            first, second = "player", "opponent"
            first_poke, second_poke = self.player, self.opponent
            first_move, second_move = player_move, opponent_move
        else:
            first, second = "opponent", "player"
            first_poke, second_poke = self.opponent, self.player
            first_move, second_move = opponent_move, player_move

        # === First Pokemon's turn ===
        first_move = self._apply_start_status(first_poke, first_move, first, events)
        if "Burn" in first_poke.start_status:
            first_poke.attack = first_poke.base_attack // 2

        self._execute_move(first_poke, second_poke, first_move, first, events)

        if self._check_faint(events):
            return self._build_response(player_move_name, opponent_move_name, events)

        # === Second Pokemon's turn ===
        second_move = self._apply_start_status(second_poke, second_move, second, events)
        if "Burn" in second_poke.start_status:
            second_poke.attack = second_poke.base_attack // 2

        # Clear flinch (only affects the slower Pokemon)
        if "Flinch" in second_poke.start_status:
            events.append(BattleEvent(
                type="status_effect", actor=second,
                message=f"{second_poke.name} flinched and couldn't move!",
            ))
            del second_poke.start_status["Flinch"]
        else:
            self._execute_move(second_poke, first_poke, second_move, second, events)

        if self._check_faint(events):
            return self._build_response(player_move_name, opponent_move_name, events)

        # === End-of-turn status damage ===
        self._apply_end_turn_damage(self.player, "player", events)
        self._apply_end_turn_damage(self.opponent, "opponent", events)
        self._check_faint(events)

        # Restore modified stats
        self.player.attack = self.player.base_attack
        self.opponent.attack = self.opponent.base_attack

        return self._build_response(player_move_name, opponent_move_name, events)

    def _find_move(self, poke: BattlePokemonRuntime, move_name: str) -> MoveInfo:
        for m in poke.moves:
            if m.name.lower() == move_name.lower():
                return m
        # Fallback to first move
        return poke.moves[0]

    def _apply_start_status(self, poke: BattlePokemonRuntime, move: MoveInfo,
                            actor: str, events: list[BattleEvent]) -> MoveInfo:
        """Apply start-of-turn status effects. May replace the move."""

        if "Paralyze" in poke.start_status:
            if random.random() < 0.25:
                events.append(BattleEvent(
                    type="status_effect", actor=actor,
                    message=f"{poke.name} is paralyzed! It can't move!",
                ))
                return MoveInfo(name="!Paralysis", type="Normal", category="Status",
                                power=0, accuracy=1.0, pp=999, description="is stunned!")

        if "Sleep" in poke.start_status:
            if poke.start_status["Sleep"]["turns"] > 0:
                poke.start_status["Sleep"]["turns"] -= 1
                events.append(BattleEvent(
                    type="status_effect", actor=actor,
                    message=f"{poke.name} is fast asleep...",
                ))
                return MoveInfo(name="!Asleep", type="Normal", category="Status",
                                power=0, accuracy=1.0, pp=999, description="is sleeping...")
            else:
                del poke.start_status["Sleep"]
                events.append(BattleEvent(
                    type="status_effect", actor=actor,
                    message=f"{poke.name} woke up!",
                ))

        if "Freeze" in poke.start_status:
            if random.random() < 0.2:
                del poke.start_status["Freeze"]
                events.append(BattleEvent(
                    type="status_effect", actor=actor,
                    message=f"{poke.name} thawed out!",
                ))
            else:
                events.append(BattleEvent(
                    type="status_effect", actor=actor,
                    message=f"{poke.name} is frozen solid!",
                ))
                return MoveInfo(name="!Freeze", type="Ice", category="Status",
                                power=0, accuracy=1.0, pp=999, description="is frozen...")

        if "Confuse" in poke.start_status:
            if poke.start_status["Confuse"]["turns"] > 0:
                poke.start_status["Confuse"]["turns"] -= 1
                if random.random() < 0.5:
                    # Hit self in confusion
                    confusion_dmg = self._calc_confusion_damage(poke)
                    poke.current_hp -= confusion_dmg
                    events.append(BattleEvent(
                        type="status_effect", actor=actor,
                        message=f"{poke.name} hurt itself in confusion for {confusion_dmg} damage!",
                        data={"damage": confusion_dmg},
                    ))
                    return MoveInfo(name="!Confuse", type="Normal", category="Status",
                                    power=0, accuracy=1.0, pp=999, description="hurt itself!")
            else:
                del poke.start_status["Confuse"]
                events.append(BattleEvent(
                    type="status_effect", actor=actor,
                    message=f"{poke.name} snapped out of confusion!",
                ))

        return move

    def _calc_confusion_damage(self, poke: BattlePokemonRuntime) -> int:
        """Calculate self-damage from confusion (40 power physical)."""
        damage = ((2 * 50 / 5 + 2) * 40 * poke.attack / poke.defense) / 50 + 2
        return max(int(damage), 1)

    def _execute_move(self, attacker: BattlePokemonRuntime, defender: BattlePokemonRuntime,
                      move: MoveInfo, actor: str, events: list[BattleEvent]) -> None:
        """Execute a move from attacker against defender."""
        defender_actor = "opponent" if actor == "player" else "player"

        # Skip pseudo-moves (status replacements like !Paralysis)
        if move.name.startswith("!"):
            return

        events.append(BattleEvent(
            type="move_use", actor=actor,
            message=f"{attacker.name} used {move.name}!",
        ))

        # Handle useless moves
        if "Useless" in move.effects:
            events.append(BattleEvent(
                type="message", actor=actor,
                message="But nothing happened!",
            ))
            return

        # Handle delayed moves
        if "Delayed" in move.effects and "Delayed" not in attacker.start_status:
            events.append(BattleEvent(
                type="message", actor=actor,
                message=f"{attacker.name} is charging up!",
            ))
            attacker.start_status["Delayed"] = move.name
            return

        # Handle instakill moves
        if "Instakill" in move.effects:
            hit_check = move.accuracy * attacker.accuracy / defender.evasion
            if random.random() > hit_check or attacker.speed < defender.speed:
                events.append(BattleEvent(type="miss", actor=actor, message="It missed!"))
            else:
                defender.current_hp = 0
                events.append(BattleEvent(
                    type="damage", actor=actor,
                    message=f"It's a one-hit KO! {defender.name} fainted!",
                    data={"damage": defender.max_hp},
                ))
            return

        # Handle multi-hit moves
        if "Multihit" in move.effects and "times" in move.effects["Multihit"]:
            times_val = move.effects["Multihit"]["times"]
            if times_val == "multiple":
                hits = random.choices([2, 3, 4, 5], weights=[3, 3, 1, 1], k=1)[0]
            else:
                hits = 2
            events.append(BattleEvent(
                type="message", actor=actor,
                message=f"It hits {hits} times!",
            ))
            total_dmg = 0
            for _ in range(hits):
                result = self._do_damage_calc(attacker, defender, move)
                total_dmg += result["damage"]
                defender.current_hp -= result["damage"]
                for ev in result["events"]:
                    events.append(BattleEvent(type=ev["type"], actor=actor,
                                              message=ev["message"], data=ev.get("data")))
                if "crash_damage" in result and result["crash_damage"]:
                    attacker.current_hp -= result["crash_damage"]
            # Status effects for multi-hit
            status_events = self._apply_move_status(attacker, defender, move)
            for ev in status_events:
                events.append(BattleEvent(type=ev["type"], actor=actor,
                                          message=ev["message"], data=ev.get("data")))
            return

        # Normal single-hit move
        result = self._do_damage_calc(attacker, defender, move)
        dmg = result["damage"]
        defender.current_hp -= dmg

        for ev in result["events"]:
            events.append(BattleEvent(type=ev["type"], actor=actor,
                                      message=ev["message"], data=ev.get("data")))

        if "crash_damage" in result and result["crash_damage"]:
            attacker.current_hp -= result["crash_damage"]

        # Recoil
        if dmg > 0 and "Recoil" in move.effects:
            recoil = max(int(dmg / 4), 1)
            attacker.current_hp -= recoil
            events.append(BattleEvent(
                type="recoil", actor=actor,
                message=f"{attacker.name} took {recoil} damage from recoil!",
                data={"damage": recoil},
            ))

        # Self-destruct
        if "SelfDestruct" in move.effects:
            attacker.current_hp = 0
            events.append(BattleEvent(
                type="faint", actor=actor,
                message=f"{attacker.name} fainted from the attack!",
            ))

        # Heal
        if dmg > 0 and "Heal" in move.effects:
            heal_type = move.effects["Heal"].get("type", "selfheal")
            if heal_type == "lifesteal":
                heal_amt = min(attacker.max_hp - attacker.current_hp, dmg // 2)
            else:
                heal_amt = min(attacker.max_hp - attacker.current_hp, attacker.max_hp // 2)
            if heal_amt > 0:
                attacker.current_hp += heal_amt
                events.append(BattleEvent(
                    type="heal", actor=actor,
                    message=f"{attacker.name} restored {heal_amt} HP!",
                    data={"healAmount": heal_amt},
                ))

        # Status effects
        status_events = self._apply_move_status(attacker, defender, move)
        for ev in status_events:
            events.append(BattleEvent(
                type=ev["type"],
                actor=actor if "attacker" not in ev.get("data", {}) else defender_actor,
                message=ev["message"], data=ev.get("data"),
            ))

    def _do_damage_calc(self, attacker: BattlePokemonRuntime,
                        defender: BattlePokemonRuntime, move: MoveInfo) -> dict:
        # Apply stat stages
        atk_stages = attacker.start_status.get("StatChange", {})
        def_stages = defender.start_status.get("StatChange", {})

        eff_attack = int(attacker.attack * STAT_STAGES.get(atk_stages.get("attack", 0), 1.0))
        eff_sp_attack = int(attacker.sp_attack * STAT_STAGES.get(atk_stages.get("spattack", 0), 1.0))
        eff_defense = int(defender.defense * STAT_STAGES.get(def_stages.get("defense", 0), 1.0))
        eff_sp_defense = int(defender.sp_defense * STAT_STAGES.get(def_stages.get("spdefense", 0), 1.0))

        return calc_damage(
            attacker_level=50,
            attacker_attack=eff_attack,
            attacker_sp_attack=eff_sp_attack,
            attacker_speed=attacker.speed,
            attacker_types=attacker.types,
            attacker_accuracy=attacker.accuracy,
            defender_defense=eff_defense,
            defender_sp_defense=eff_sp_defense,
            defender_types=defender.types,
            defender_evasion=defender.evasion,
            move_power=move.power,
            move_type=move.type,
            move_category=move.category,
            move_accuracy=move.accuracy,
            move_effects=move.effects,
        )

    def _apply_move_status(self, attacker: BattlePokemonRuntime,
                           defender: BattlePokemonRuntime, move: MoveInfo) -> list[dict]:
        return apply_status_effects(
            move_effects=move.effects,
            move_name=move.name,
            attacker_name=attacker.name,
            attacker_types=attacker.types,
            attacker_start_status=attacker.start_status,
            attacker_end_status=attacker.end_status,
            defender_name=defender.name,
            defender_types=defender.types,
            defender_start_status=defender.start_status,
            defender_end_status=defender.end_status,
        )

    def _apply_end_turn_damage(self, poke: BattlePokemonRuntime,
                               actor: str, events: list[BattleEvent]) -> None:
        """Apply end-of-turn burn/poison damage (1/16 max HP)."""
        if "Burn" in poke.end_status or "Poison" in poke.end_status:
            dmg = max(poke.max_hp // 16, 1)
            poke.current_hp -= dmg
            status_name = "burn" if "Burn" in poke.end_status else "poison"
            events.append(BattleEvent(
                type="status_effect", actor=actor,
                message=f"{poke.name} took {dmg} damage from {status_name}!",
                data={"damage": dmg},
            ))

    def _check_faint(self, events: list[BattleEvent]) -> bool:
        """Check if either Pokemon has fainted. Sets battle_over and winner."""
        if self.player.current_hp <= 0:
            self.battle_over = True
            self.winner = "opponent"
            events.append(BattleEvent(
                type="faint", actor="player",
                message=f"{self.player.name} fainted!",
            ))
            events.append(BattleEvent(
                type="message", actor="opponent",
                message=f"{self.opponent.name} wins!",
            ))
            return True
        if self.opponent.current_hp <= 0:
            self.battle_over = True
            self.winner = "player"
            events.append(BattleEvent(
                type="faint", actor="opponent",
                message=f"{self.opponent.name} fainted!",
            ))
            events.append(BattleEvent(
                type="message", actor="player",
                message=f"{self.player.name} wins!",
            ))
            return True
        return False

    def _build_response(self, player_move: str, opponent_move: str,
                        events: list[BattleEvent]) -> BattleMoveResponse:
        return BattleMoveResponse(
            turnNumber=self.turn_number,
            playerMove=player_move,
            opponentMove=opponent_move,
            events=events,
            player=self.player.to_state(),
            opponent=self.opponent.to_state(),
            battleOver=self.battle_over,
            winner=self.winner,
        )


def create_battle_pokemon(name: str, selected_moves: list[str]) -> BattlePokemonRuntime:
    """Create a BattlePokemonRuntime from game data."""
    raw = game_data.pokemon_raw[name]
    move_objects = []
    for m_name in selected_moves:
        key = m_name.lower()
        if key in game_data.moves:
            move_objects.append(copy.deepcopy(game_data.moves[key]))
    if not move_objects:
        # Fallback: use first available move
        for m_name in raw["moveset"][:4]:
            key = m_name.lower()
            if key in game_data.moves:
                move_objects.append(copy.deepcopy(game_data.moves[key]))

    return BattlePokemonRuntime(
        name=name,
        types=raw["types"],
        sprite_url=raw["spriteUrl"],
        hp=raw["hp"],
        attack=raw["attack"],
        defense=raw["defense"],
        sp_attack=raw["spAttack"],
        sp_defense=raw["spDefense"],
        speed=raw["speed"],
        moves=move_objects,
    )
