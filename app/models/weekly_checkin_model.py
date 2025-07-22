from typing import Optional
from sqlmodel import SQLModel, Field, Column, ForeignKey
from sqlalchemy import Boolean, Date


class WeeklyCheckIn(SQLModel, table=True):
    __tablename__ = "weekly_checkins"

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(
        sa_column=Column(
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
    )

    week_start_date: Date = Field(sa_column=Column(Date, nullable=False))

    mon: bool = Field(sa_column=Column(Boolean, nullable=False, default=False))
    tue: bool = Field(sa_column=Column(Boolean, nullable=False, default=False))
    wed: bool = Field(sa_column=Column(Boolean, nullable=False, default=False))
    thu: bool = Field(sa_column=Column(Boolean, nullable=False, default=False))
    fri: bool = Field(sa_column=Column(Boolean, nullable=False, default=False))
    sat: bool = Field(sa_column=Column(Boolean, nullable=False, default=False))
    sun: bool = Field(sa_column=Column(Boolean, nullable=False, default=False))
