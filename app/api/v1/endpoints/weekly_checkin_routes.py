from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.database import get_session
from app.crud.weekly_checkin_crud import (
    crud_check_in,
    crud_get_latest_check_in,
    crud_perfect_reward_weekly_checkin,
)
from app.schemas.weekly_checkin_schema import (
    PerfectWeeklyCheckInRewardRead,
    WeeklyCheckInRead,
)

router = APIRouter(dependencies=[Depends(get_session), Depends(get_current_user)])


@router.post("/check_in/{player_id}", response_model=WeeklyCheckInRead)
async def check_in(player_id: int, session: AsyncSession = Depends(get_session)):
    return await crud_check_in(player_id, session)


@router.get("/check_in/latest/{player_id}", response_model=WeeklyCheckInRead)
async def get_latest_check_in(
    player_id: int, session: AsyncSession = Depends(get_session)
):
    return await crud_get_latest_check_in(player_id, session)


@router.post(
    "/check_in/reward/{player_id}", response_model=PerfectWeeklyCheckInRewardRead
)
async def get_reward_perfect_weekly_check_in(
    player_id: int, session: AsyncSession = Depends(get_session)
):
    return await crud_perfect_reward_weekly_checkin(player_id, session)
