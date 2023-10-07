from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
POKEMON_CSV = DATA_DIR / "pokemon.csv"
MOVES_CSV = DATA_DIR / "moves.csv"

DEFAULT_LEVEL = 50

BLACKLIST = [
    "Razorwind", "Whirlwind", "Fly", "Bind", "Wrap", "Thrash", "Roar",
    "SonicBoom", "Disable", "Mist", "LowKick", "Counter", "SeismicToss",
    "LeechSeed", "PetalDance", "DragonRage", "FireSpin", "Dig", "Toxic",
    "Rage", "Teleport", "NightShade", "Mimic", "LightScreen", "Haze",
    "Reflect", "FocusEnergy", "Bide", "Metronome", "MirrorMove", "Clamp",
    "DreamEater", "SkyAttack", "Transform", "Psywave", "Splash", "Rest",
    "Conversion", "SuperFang", "Substitute",
]
