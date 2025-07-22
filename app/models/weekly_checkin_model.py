from datetime import date
from typing import TYPE_CHECKING, Optional
from sqlmodel import Relationship, SQLModel, Field, Column, ForeignKey
from sqlalchemy import Boolean, Date

if TYPE_CHECKING:
    from app.models import Player


class WeeklyCheckIn(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)

    player_id: int = Field(
        sa_column=Column(
            ForeignKey("player.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
    )

    week_start_date: date = Field(sa_column=Column(Date, nullable=False))

    mon: bool = Field(sa_column=Column(Boolean, nullable=False, default=False))
    tue: bool = Field(sa_column=Column(Boolean, nullable=False, default=False))
    wed: bool = Field(sa_column=Column(Boolean, nullable=False, default=False))
    thu: bool = Field(sa_column=Column(Boolean, nullable=False, default=False))
    fri: bool = Field(sa_column=Column(Boolean, nullable=False, default=False))
    sat: bool = Field(sa_column=Column(Boolean, nullable=False, default=False))
    sun: bool = Field(sa_column=Column(Boolean, nullable=False, default=False))

    player: Optional["Player"] = Relationship(back_populates="weekly_checkins")
