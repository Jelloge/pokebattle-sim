from pydantic import BaseModel


class PokemonStats(BaseModel):
    hp: int
    attack: int
    defense: int
    spAttack: int
    spDefense: int
    speed: int


class PokemonSummary(BaseModel):
    id: int
    name: str
    types: list[str]
    spriteUrl: str
    statTotal: int


class PokemonDetail(BaseModel):
    id: int
    name: str
    types: list[str]
    spriteUrl: str
    stats: PokemonStats
    moves: list[str]  # available move names
