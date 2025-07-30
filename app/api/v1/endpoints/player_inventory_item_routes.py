from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.core.auth import get_current_user
from app.crud.player_inventory_item_crud import (
    crud_get_rewards,
    crud_get_inventory,
    crud_check_has_item,
    crud_check_has_quantity,
    crud_use_item,
    crud_equip_item,
    crud_unequip_item,
)
from app.schemas.player_inventory_item_schema import PlayerInventoryItemRead
from app.schemas.reward_schema import RewardRead

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/rewards", response_model=List[RewardRead])
async def get_rewards(session: Session = Depends(get_session)):
    return await crud_get_rewards(session)


@router.get(
    "/player/{player_id}/inventory", response_model=List[PlayerInventoryItemRead]
)
async def get_player_inventory(player_id: int, session: Session = Depends(get_session)):
    return await crud_get_inventory(session, player_id)


@router.get("/player/{player_id}/owns/{reward_id}", response_model=bool)
async def check_owns_item(
    player_id: int, reward_id: int, session: Session = Depends(get_session)
):
    return await crud_check_has_item(session, player_id, reward_id)


@router.get(
    "/player/{player_id}/has_quantity/{reward_id}/{min_quantity}", response_model=bool
)
async def check_has_quantity(
    player_id: int,
    reward_id: int,
    min_quantity: int,
    session: Session = Depends(get_session),
):
    return await crud_check_has_quantity(session, player_id, reward_id, min_quantity)


@router.post("/player/{player_id}/use/{reward_id}")
async def use_item(
    player_id: int, reward_id: int, session: Session = Depends(get_session)
):
    await crud_use_item(session, player_id, reward_id)
    return {"status": "used"}


@router.post("/equip/{item_id}")
async def equip_item(item_id: int, slot: str, session: Session = Depends(get_session)):
    await crud_equip_item(session, item_id, slot)
    return {"status": "equipped"}


@router.post("/unequip/{item_id}")
async def unequip_item(item_id: int, session: Session = Depends(get_session)):
    await crud_unequip_item(session, item_id)
    return {"status": "unequipped"}
