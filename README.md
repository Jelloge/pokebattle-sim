# PokeBattle Sim

A Gen 1 Pokemon battle simulator with an AI opponent, animated battles, and post-battle analytics. Built with a modern full-stack architecture: **React + TypeScript** frontend and **FastAPI** (Python) backend.

## Features

- **151 Gen 1 Pokemon** with accurate base stats, types, and movesets scraped from Bulbapedia
- **AI Opponent** that selects a stat-matched Pokemon and chooses moves using a weighted scoring system (damage potential, status value, healing priority, and context bonuses)
- **Accurate Gen 1 Damage Formula** including STAB, type effectiveness, critical hits, and stat stages
- **Status Effects** &mdash; Burn, Poison, Paralyze, Sleep, Freeze, Confusion, Flinch, and stat modifiers
- **Battle Animations** &mdash; attack lunge, damage shake, super-effective flash, faint, and HP bar transitions via CSS keyframes
- **Battle Analytics** &mdash; interactive charts (HP over time, damage per turn, move effectiveness pie charts, move usage tables) powered by Recharts
- **Dark Theme** with pixel font styling

## Tech Stack

| Layer      | Technology                        |
| ---------- | --------------------------------- |
| Frontend   | React 19, TypeScript, Vite        |
| Styling    | CSS custom properties, keyframes  |
| Charts     | Recharts                          |
| Routing    | React Router v7                   |
| HTTP       | Axios                             |
| Backend    | FastAPI, Pydantic                 |
| Testing    | pytest, httpx                     |
| Data       | CSV (pokemon.csv, moves.csv)      |

## Project Structure

```
pokesim/
├── backend/
│   ├── app/
│   │   ├── core/           # Battle engine fundamentals
│   │   │   ├── damage.py       # Gen 1 damage formula
│   │   │   ├── effects.py      # Move effect parser
│   │   │   ├── stat_calc.py    # HP/stat calculators
│   │   │   ├── status.py       # Status effect application
│   │   │   └── type_chart.py   # 18x18 type effectiveness table
│   │   ├── models/         # Pydantic request/response models
│   │   │   ├── battle.py       # Battle state, events, analytics
│   │   │   ├── move.py         # Move info
│   │   │   └── pokemon.py      # Pokemon summary/detail
│   │   ├── routers/        # API endpoints
│   │   │   ├── analytics.py    # GET /api/battle/{id}/analytics
│   │   │   ├── battle.py       # POST /api/battle/start, /api/battle/move
│   │   │   └── pokemon.py      # GET /api/pokemon, /api/pokemon/{id}
│   │   ├── services/       # Business logic
│   │   │   ├── ai_service.py       # AI opponent selection & move choice
│   │   │   ├── analytics_service.py # Per-turn stat tracking
│   │   │   ├── battle_service.py    # Turn execution state machine
│   │   │   └── data_loader.py      # CSV loading & singleton cache
│   │   ├── config.py       # Constants & blacklisted moves
│   │   └── main.py         # FastAPI app entry point
│   ├── data/
│   │   ├── moves.csv        # 165 Gen 1 moves
│   │   └── pokemon.csv      # 151 Gen 1 Pokemon
│   ├── tests/               # 17 tests (damage, battle, AI)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/             # Axios client & API functions
│   │   ├── components/
│   │   │   ├── analytics/   # BattleSummary, DamageChart, EffectivenessChart
│   │   │   ├── battle/      # BattleScene, HealthBar, MovePanel, WinOverlay, ...
│   │   │   ├── layout/      # Header, Layout
│   │   │   └── pokemon/     # PokemonCard, PokemonGrid, MoveSelector, TypeBadge, ...
│   │   ├── hooks/           # useBattle, usePokemonList
│   │   ├── pages/           # SelectionPage, BattlePage, AnalyticsPage
│   │   ├── styles/          # global.css, animations.css
│   │   └── utils/           # typeColors.ts
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
└── README.md
```

## Getting Started

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** and npm

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8000
```

The API will be available at `http://localhost:8000`. You can view the auto-generated docs at `http://localhost:8000/docs`.

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.

### Running Tests

```bash
cd backend
python -m pytest tests/ -v
```

## How to Play

1. **Select a Pokemon** &mdash; browse or filter by type, then click to view available moves
2. **Choose up to 4 moves** &mdash; the move list shows type, power, and PP
3. **Click Battle** &mdash; the AI picks an opponent matched to your stat total
4. **Choose moves each turn** &mdash; watch animations play out as damage, status effects, and crits unfold
5. **View Analytics** after the battle ends &mdash; see HP charts, effectiveness breakdowns, and move usage stats

## API Reference

| Method | Endpoint                        | Description              |
| ------ | ------------------------------- | ------------------------ |
| GET    | `/api/pokemon`                  | List all 151 Pokemon     |
| GET    | `/api/pokemon/{id}`             | Pokemon detail + stats   |
| GET    | `/api/pokemon/{id}/moves`       | Available moves for a Pokemon |
| POST   | `/api/battle/start`             | Start a new battle       |
| POST   | `/api/battle/move`              | Execute a turn           |
| GET    | `/api/battle/{id}/analytics`    | Get battle analytics     |

## AI Opponent Logic

The AI uses a weighted scoring system rather than random selection:

- **Damage Score** (0-100): Estimates damage output considering type effectiveness and STAB
- **Status Score** (0-40): Values status moves (burn, paralyze, stat boosts) when conditions are favorable
- **Healing Score** (0-35): Prioritizes healing when HP is low
- **Context Bonuses**: Extra weight for finishing moves when opponent HP is low
- **Noise** (&plusmn;5): Small random factor to prevent perfectly predictable play

## Bugs Fixed from Original

The original codebase had 6 bugs that were identified and fixed:

1. Wrong variable reference for Delayed status (used attacker instead of defender)
2. Speed comparison typo (`lower` instead of `slower`)
3. Wrong `max_health` reference for burn/poison damage calculation
4. Incorrect dict deletion for Freeze thaw (deleted from `effects` instead of `start_status`)
5. Permanent moveset mutation across battles (missing deep copy)
6. Double random factor in damage calculation (applied twice instead of once)
