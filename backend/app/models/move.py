from pydantic import BaseModel


class MoveInfo(BaseModel):
    name: str
    type: str
    category: str  # Physical | Special | Status
    power: int
    accuracy: float
    pp: int
    description: str
    effects: dict = {}
