from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud.weekly_checkin_crud import crud_check_in, crud_get_latest_check_in
from app.schemas.weekly_checkin_schema import WeeklyCheckInRead

router = APIRouter()


@router.post("/check_in/{player_id}", response_model=WeeklyCheckInRead)
async def check_in(player_id: int, session: AsyncSession = Depends(get_session)):
    return await crud_check_in(player_id, session)


@router.get("/check_in/latest/{player_id}", response_model=WeeklyCheckInRead)
async def get_latest_check_in(
    player_id: int, session: AsyncSession = Depends(get_session)
):
    return await crud_get_latest_check_in(player_id, session)
