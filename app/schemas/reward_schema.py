from pydantic import BaseModel
from typing import Optional


class RewardRead(BaseModel):
    id: int
    name: str
    description: str
    type: str
    stackable: bool
    equipped_image_url: Optional[str]
    image_url: Optional[str]
