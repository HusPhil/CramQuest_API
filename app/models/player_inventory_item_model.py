from enum import Enum
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, ForeignKey

if TYPE_CHECKING:
    from app.models import Player, Reward


class EquippedSlot(str, Enum):
    HEAD = "head"
    BODY = "body"
    SKIN = "skin"
    WEAPON = "weapon"


class PlayerInventoryItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    player_id: int = Field(
        foreign_key="player.id",
        nullable=False,
        index=True,
    )
    reward_id: int = Field(
        foreign_key="reward.id",
        nullable=False,
    )

    quantity: int = 1
    equipped_slot: Optional[EquippedSlot] = Field(default=None)

    player: "Player" = Relationship(back_populates="inventory_items")
    reward: "Reward" = Relationship(back_populates="inventory_items")
