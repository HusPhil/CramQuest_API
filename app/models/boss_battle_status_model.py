from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, ForeignKey, String, DateTime

if TYPE_CHECKING:
    from app.models import Player


class BossBattleStatusState(str):
    AVAILABLE = "available"
    DEFEATED = "defeated"
    LOCKED = "locked"


class BossBattleStatus(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    player_id: int = Field(
        sa_column=Column(
            ForeignKey("player.id", ondelete="CASCADE"), nullable=False, index=True
        )
    )

    status: str = Field(
        sa_column=Column(String, nullable=False), default=BossBattleStatusState.LOCKED
    )

    available_at: Optional[datetime] = Field(
        default=None, sa_type=DateTime(timezone=True), nullable=True
    )
    defeated_at: Optional[datetime] = Field(
        default=None, sa_type=DateTime(timezone=True), nullable=True
    )

    player: "Player" = Relationship(back_populates="boss_battle_statuses")
