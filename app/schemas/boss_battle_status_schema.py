from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.schemas.reward_schema import RewardItemRead


class BossBattleStatusBase(BaseModel):
    status: str
    available_at: Optional[datetime] = None
    defeated_at: Optional[datetime] = None


class BossBattleStatusRead(BossBattleStatusBase):
    id: int
    player_id: int


class BossBattleEndRead(BaseModel):
    base_xp: int
    bonus_xp: int
    reward_item: Optional[RewardItemRead]


class BossBattlEndInfo(BaseModel):
    id: int
    victory: bool
    total_rounds: int
    player_health: int
    enemy_health: int
