from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.core.auth import get_current_user
from app.schemas.boss_battle_status_schema import BossBattleStatusRead
from app.crud.boss_battle_status_crud import (
    crud_read_player_boss_battle_statuses,
    crud_read_player_boss_battle_status,
    crud_read_player_latest_boss_battle_status,
)
from app.models import User

router = APIRouter(
    prefix="/boss-battle-statuses",
    tags=["Boss Battle Statuses"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/player/{player_id}", response_model=List[BossBattleStatusRead])
async def get_player_boss_battle_statuses(
    player_id: int, session: Session = Depends(get_session)
):
    return await crud_read_player_boss_battle_statuses(session, player_id)


@router.get("/{status_id}", response_model=BossBattleStatusRead)
async def get_player_boss_battle_status(
    status_id: int, session: Session = Depends(get_session)
):
    status = await crud_read_player_boss_battle_status(session, status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Boss battle status not found")
    return status


@router.get("/player/{player_id}/latest", response_model=BossBattleStatusRead)
async def get_player_latest_boss_battle_status(
    player_id: int, session: Session = Depends(get_session)
):
    status = await crud_read_player_latest_boss_battle_status(session, player_id)
    if not status:
        raise HTTPException(status_code=404, detail="No boss battle status found")
    return status
