from pydantic import BaseModel
from typing import Optional


class PlayerInventoryItemRead(BaseModel):
    id: int
    player_id: int
    reward_id: int
    quantity: int
    equipped_slot: Optional[str]
