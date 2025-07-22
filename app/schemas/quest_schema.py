from typing import Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class QuestStatus(str, Enum):
    TO_DO = "to_do"
    DOING = "doing"
    DONE = "done"
    ARCHIVE = "archive"


class QuestBase(BaseModel):
    subject_id: int
    description: str = Field(None, min_length=1, max_length=255)
    difficulty: int = Field(..., ge=1, le=5, description="Difficulty level (1 to 5)")
    status: QuestStatus = QuestStatus.TO_DO


class QuestCreate(QuestBase):
    pass


class QuestRead(QuestBase):
    id: int
    created_at: datetime


class QuestUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    difficulty: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[QuestStatus] = None
