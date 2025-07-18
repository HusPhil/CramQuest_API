from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, String, ForeignKey
from enum import Enum

from app.external.external import get_player_initial_next_lvl_xp


if TYPE_CHECKING:
    from app.models import User, Profile, StudySession, Subject


class PlayerTitle(str, Enum):
    NOVICE = "Novice"
    APPRENTICE = "Apprentice"
    ADEPT = "Adept"
    SCHOLAR = "Scholar"
    SAGE = "Sage"
    ARCHMAGE = "Archmage"
    OMNISCIENT = "Omniscient"


class Player(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(
        sa_column=Column(
            ForeignKey("user.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
            index=True,
        )
    )
    title: PlayerTitle = Field(
        sa_column=Column(String, nullable=False), default=PlayerTitle.NOVICE
    )
    level: int = Field(default=1)
    experience: int = Field(default=0)
    next_level_xp: int = Field(default=195)

    session_streak: int = Field(default=0)
    longest_session_streak: int = Field(default=0)

    daily_streak: int = Field(default=0)
    longest_daily_streak: int = Field(default=0)

    study_sessions: list["StudySession"] = Relationship(
        back_populates="player", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    user: "User" = Relationship(back_populates="player")
    profile: Optional["Profile"] = Relationship(
        back_populates="player", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    subjects: list["Subject"] = Relationship(
        back_populates="player", sa_relationship_kwargs={"cascade": "all, delete"}
    )
