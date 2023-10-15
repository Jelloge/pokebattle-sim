"""Battle analytics tracking and computation."""

from app.models.battle import (
    BattleAnalytics, SideAnalytics, TurnAnalytics,
    BattleEvent, BattleMoveResponse,
)


class AnalyticsTracker:
    """Tracks analytics for a single battle."""

    def __init__(self, battle_id: str, player_name: str, opponent_name: str) -> None:
        self.battle_id = battle_id
        self.player = SideAnalytics(pokemonName=player_name)
        self.opponent = SideAnalytics(pokemonName=opponent_name)
        self.turns: list[TurnAnalytics] = []
        self.winner: str | None = None

    def record_turn(self, response: BattleMoveResponse,
                    player_max_hp: int, opponent_max_hp: int) -> None:
        """Record analytics from a turn result."""
        player_dmg = 0
        opponent_dmg = 0

        for event in response.events:
            self._process_event(event)

            # Track damage per side
            if event.type == "damage" and event.data:
                dmg = event.data.get("damage", 0)
                if event.actor == "player":
                    player_dmg += dmg
                else:
                    opponent_dmg += dmg

        # Record move usage
        self.player.movesUsed[response.playerMove] = \
            self.player.movesUsed.get(response.playerMove, 0) + 1
        self.opponent.movesUsed[response.opponentMove] = \
            self.opponent.movesUsed.get(response.opponentMove, 0) + 1

        # Update totals
        self.player.totalDamageDealt += player_dmg
        self.player.totalDamageTaken += opponent_dmg
        self.opponent.totalDamageDealt += opponent_dmg
        self.opponent.totalDamageTaken += player_dmg

        # Record turn
        self.turns.append(TurnAnalytics(
            turnNumber=response.turnNumber,
            playerMove=response.playerMove,
            opponentMove=response.opponentMove,
            playerDamageDealt=player_dmg,
            opponentDamageDealt=opponent_dmg,
            playerHpAfter=response.player.currentHp,
            opponentHpAfter=response.opponent.currentHp,
        ))

        if response.battleOver:
            self.winner = response.winner

    def _process_event(self, event: BattleEvent) -> None:
        side = self.player if event.actor == "player" else self.opponent

        if event.type == "critical":
            side.criticalHits += 1

        elif event.type == "miss":
            side.missCount += 1

        elif event.type == "effectiveness" and event.data:
            eff = event.data.get("effectiveness", "normal")
            if eff == "super":
                side.superEffectiveHits += 1
            elif eff == "not_very":
                side.notVeryEffectiveHits += 1

        elif event.type == "status_inflict" and event.data:
            status = event.data.get("statusEffect", "")
            if status and status not in side.statusesInflicted:
                side.statusesInflicted.append(status)

    def get_analytics(self) -> BattleAnalytics:
        return BattleAnalytics(
            battleId=self.battle_id,
            totalTurns=len(self.turns),
            winner=self.winner,
            playerAnalytics=self.player,
            opponentAnalytics=self.opponent,
            turnLog=self.turns,
        )
