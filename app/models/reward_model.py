from enum import Enum
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models import PlayerInventoryItem


class RewardType(str, Enum):
    ARMOR = "armor"
    SKIN = "skin"
    POTION = "potion"
    MISC = "misc"


class RewardRarity(str, Enum):
    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class Reward(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    type: RewardType = Field()
    rarity: RewardRarity = Field()
    stackable: bool = True
    image_url: Optional[str] = None
    equipped_image_url: Optional[str] = None

    inventory_items: list["PlayerInventoryItem"] = Relationship(back_populates="reward")
