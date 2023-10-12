"""Load Pokemon and Move data from CSV files."""

import csv
from app.config import POKEMON_CSV, MOVES_CSV, BLACKLIST, DEFAULT_LEVEL
from app.core.stat_calc import calc_hp, calc_stat
from app.core.effects import parse_effects
from app.models.move import MoveInfo
from app.models.pokemon import PokemonSummary, PokemonDetail, PokemonStats


class GameData:
    """Holds all loaded game data."""

    def __init__(self) -> None:
        self.moves: dict[str, MoveInfo] = {}
        self.move_effects: dict[str, dict] = {}
        self.pokemon_summaries: list[PokemonSummary] = []
        self.pokemon_details: dict[str, PokemonDetail] = {}
        # Raw base stats for battle calculations
        self.pokemon_raw: dict[str, dict] = {}

    def load(self) -> None:
        self._load_moves()
        self._load_pokemon()

    def _load_moves(self) -> None:
        with open(MOVES_CSV, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            for row in reader:
                if len(row) < 8:
                    continue
                name = row[1]
                if name in BLACKLIST:
                    continue
                desc = row[7].replace(";", ".")
                effects = parse_effects(desc)
                move = MoveInfo(
                    name=name,
                    type=row[2],
                    category=row[3],
                    pp=int(row[4]),
                    power=int(row[5]),
                    accuracy=float(row[6]),
                    description=desc,
                    effects=effects,
                )
                self.moves[name.lower()] = move
                self.move_effects[name.lower()] = effects

    def _load_pokemon(self) -> None:
        with open(POKEMON_CSV, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            for row in reader:
                if len(row) < 11:
                    continue
                pokedex_id = int(row[0])
                name = row[1]
                types = row[2].split(";")
                base_hp = int(row[3])
                base_atk = int(row[4])
                base_def = int(row[5])
                base_spa = int(row[6])
                base_spd = int(row[7])
                base_spe = int(row[8])
                # Use PokeAPI sprites (reliable, always available)
                sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokedex_id}.png"
                moveset_raw = row[9].split(";") if row[9] else []
                moveset = [m for m in moveset_raw if m not in BLACKLIST]

                # Compute stats at default level
                hp = calc_hp(base_hp, DEFAULT_LEVEL)
                atk = calc_stat(base_atk, DEFAULT_LEVEL)
                defense = calc_stat(base_def, DEFAULT_LEVEL)
                spa = calc_stat(base_spa, DEFAULT_LEVEL)
                spdef = calc_stat(base_spd, DEFAULT_LEVEL)
                speed = calc_stat(base_spe, DEFAULT_LEVEL)

                stats = PokemonStats(
                    hp=hp, attack=atk, defense=defense,
                    spAttack=spa, spDefense=spdef, speed=speed,
                )
                stat_total = hp + atk + defense + spa + spdef + speed

                # Filter moveset to only include moves we have loaded
                available_moves = [m for m in moveset if m.lower() in self.moves]

                summary = PokemonSummary(
                    id=pokedex_id, name=name, types=types,
                    spriteUrl=sprite_url, statTotal=stat_total,
                )
                detail = PokemonDetail(
                    id=pokedex_id, name=name, types=types,
                    spriteUrl=sprite_url, stats=stats,
                    moves=available_moves,
                )

                self.pokemon_summaries.append(summary)
                self.pokemon_details[name] = detail
                self.pokemon_raw[name] = {
                    "types": types,
                    "spriteUrl": sprite_url,
                    "hp": hp,
                    "attack": atk,
                    "defense": defense,
                    "spAttack": spa,
                    "spDefense": spdef,
                    "speed": speed,
                    "statTotal": stat_total,
                    "moveset": available_moves,
                }


# Singleton instance
game_data = GameData()
