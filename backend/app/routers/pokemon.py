from fastapi import APIRouter, HTTPException
from app.services.data_loader import game_data
from app.models.pokemon import PokemonSummary, PokemonDetail
from app.models.move import MoveInfo

router = APIRouter(prefix="/api/pokemon", tags=["pokemon"])


@router.get("", response_model=list[PokemonSummary])
def list_pokemon():
    return game_data.pokemon_summaries


@router.get("/{pokemon_id}", response_model=PokemonDetail)
def get_pokemon(pokemon_id: int):
    for detail in game_data.pokemon_details.values():
        if detail.id == pokemon_id:
            return detail
    raise HTTPException(status_code=404, detail="Pokemon not found")


@router.get("/{pokemon_id}/moves", response_model=list[MoveInfo])
def get_pokemon_moves(pokemon_id: int):
    for detail in game_data.pokemon_details.values():
        if detail.id == pokemon_id:
            moves = []
            for m_name in detail.moves:
                key = m_name.lower()
                if key in game_data.moves:
                    moves.append(game_data.moves[key])
            return moves
    raise HTTPException(status_code=404, detail="Pokemon not found")
