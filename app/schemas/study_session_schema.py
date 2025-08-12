from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from app.models.study_session_model import SessionStatus
from app.schemas.quest_schema import QuestRead
from app.schemas.task_schema import TaskRead, TaskTimingBatchPayload


class StudySessionCreate(BaseModel):
    """Schema for creating a study session."""

    player_id: int
    quest_id: int
    subject_id: int
    duration_mins: int = Field(..., gt=0)
    tasks_to_create: list[str]


class StudySessionRead(BaseModel):
    """Schema for returning study session details."""

    id: int
    player_id: int
    quest_id: int
    subject_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    actual_complete_time: Optional[datetime] = None
    bonus_xp: int
    base_xp: int
    status: SessionStatus
    tasks: list[TaskRead]


class StudySessionEnd(StudySessionRead):
    """Schema for ending a study session."""

    session_streak: int
    longest_session_streak: int
    is_boss_available: bool


class StudySessionResume(BaseModel):
    session_data: Optional[StudySessionRead] = None
    quest_data: Optional[QuestRead] = None
    is_resumable: bool
