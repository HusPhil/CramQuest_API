from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BossBattleStatusBase(BaseModel):
    status: str
    available_at: Optional[datetime] = None
    defeated_at: Optional[datetime] = None


class BossBattleStatusRead(BossBattleStatusBase):
    id: int
    player_id: int
