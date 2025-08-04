from pydantic import BaseModel
from typing import Optional

from app.models.reward_model import RewardRarity


class RewardItemRead(BaseModel):
    id: int
    name: str
    description: str
    type: str
    rarity: RewardRarity
    stackable: bool
    equipped_image_url: Optional[str]
    image_url: Optional[str]
