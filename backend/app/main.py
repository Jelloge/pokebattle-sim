from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.data_loader import game_data
from app.routers import pokemon, battle, analytics

app = FastAPI(title="PokeBattle Sim", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pokemon.router)
app.include_router(battle.router)
app.include_router(analytics.router)


@app.on_event("startup")
def startup():
    game_data.load()


@app.get("/api/health")
def health():
    return {"status": "ok", "pokemon_count": len(game_data.pokemon_summaries)}
