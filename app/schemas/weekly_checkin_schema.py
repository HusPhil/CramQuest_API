from enum import Enum
from pydantic import BaseModel


class CheckInStatus(BaseModel):
    is_checked: bool
    is_future: bool


class WeeklyCheckInRead(BaseModel):
    id: int
    player_id: int
    week_start_date: str
    monday: CheckInStatus
    tuesday: CheckInStatus
    wednesday: CheckInStatus
    thursday: CheckInStatus
    friday: CheckInStatus
    saturday: CheckInStatus
    sunday: CheckInStatus
