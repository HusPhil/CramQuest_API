from enum import Enum
from pydantic import BaseModel
from typing import Optional
from app.schemas.reward_schema import RewardItemRead


class ItemUses(str, Enum):
    EQUIP = "equipped"
    UNEQUIP = "unequipped"
    USE = "used"


class PlayerInventoryItemRead(BaseModel):
    id: int
    player_id: int
    reward_id: int
    quantity: int
    equipped_slot: Optional[str]
    item: RewardItemRead


class EquipSkinRequest(BaseModel):
    skin_url: str


class UseItemResponse(BaseModel):
    status: ItemUses
