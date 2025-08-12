from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.core.auth import get_current_user
from app.schemas.boss_battle_status_schema import (
    BossBattleEndRead,
    BossBattlEndInfo,
    BossBattleStatusRead,
)
from app.crud.boss_battle_status_crud import (
    crud_end_boss_battle,
    crud_read_player_boss_battle_statuses,
    crud_read_player_boss_battle_status,
    crud_read_player_latest_boss_battle_status,
    crud_start_boss_battle,
)
from app.models import User

router = APIRouter(
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
    status = await crud_read_player_latest_boss_battle_status(player_id, session)
    if not status:
        raise HTTPException(status_code=404, detail="No boss battle status found")
    return status


@router.post("/player/{player_id}/end", response_model=BossBattleEndRead)
async def boss_battle_end(
    player_id: int,
    battle_info: BossBattlEndInfo,
    session: Session = Depends(get_session),
):
    print("Processing end of boss battle for player:", player_id, battle_info)
    return await crud_end_boss_battle(player_id, battle_info, session)


@router.post("/player/{battle_id}/start", response_model=BossBattleStatusRead)
async def boss_battle_start(
    battle_id: int,
    session: Session = Depends(get_session),
):
    return await crud_start_boss_battle(battle_id, session)
