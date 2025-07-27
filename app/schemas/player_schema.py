from datetime import date
from pydantic import BaseModel, Field
from webob import week
from app.models.player_model import PlayerTitle
from typing import Optional


class PlayerBase(BaseModel):
    title: PlayerTitle
    level: int
    experience: int
    next_level_xp: int
    session_streak: int
    longest_session_streak: int
    daily_streak: int
    longest_daily_streak: int
    weekly_streak: int
    longest_weekly_streak: int
    last_checkin_date: Optional[date]
    last_week_checkin_date: Optional[date]


class PlayerCreate(BaseModel):
    title: PlayerTitle = Field(
        default=PlayerTitle.NOVICE, description="Choose a player title"
    )
    level: Optional[int] = 1
    experience: Optional[int] = 0


class PlayerRead(PlayerBase):
    id: int
    user_id: int
