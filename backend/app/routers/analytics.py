from fastapi import APIRouter, HTTPException
from app.models.battle import BattleAnalytics
from app.routers.battle import active_analytics

router = APIRouter(prefix="/api/battle", tags=["analytics"])


@router.get("/{battle_id}/analytics", response_model=BattleAnalytics)
def get_analytics(battle_id: str):
    tracker = active_analytics.get(battle_id)
    if not tracker:
        raise HTTPException(status_code=404, detail="Battle analytics not found")
    return tracker.get_analytics()
