from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.core.auth import get_current_admin, get_current_user
from app.crud.player_inventory_item_crud import (
    crud_equip_skin,
    crud_get_rewards,
    crud_get_player_inventory,
    crud_check_has_item,
    crud_check_has_quantity,
    crud_unequip_skin,
    crud_use_item,
    crud_equip_item,
    crud_unequip_item,
    crud_get_player_skins,
)
from app.schemas.player_inventory_item_schema import (
    PlayerInventoryItemRead,
    UseItemResponse,
    EquipSkinRequest,
)
from app.schemas.reward_schema import RewardItemRead
from app.models import User

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/rewards", response_model=List[RewardItemRead])
async def get_rewards(
    session: Session = Depends(get_session),
    admin_user: User = Depends(get_current_admin),
):
    return await crud_get_rewards(session)


@router.get(
    "/player/{player_id}/inventory", response_model=List[PlayerInventoryItemRead]
)
async def get_player_inventory(player_id: int, session: Session = Depends(get_session)):
    return await crud_get_player_inventory(session, player_id)


@router.get("/player/{player_id}/skins", response_model=List[PlayerInventoryItemRead])
async def get_player_skins(player_id: int, session: Session = Depends(get_session)):
    return await crud_get_player_skins(session, player_id)


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


@router.post("/player/{player_id}/use/{reward_id}", response_model=UseItemResponse)
async def use_item(
    player_id: int, reward_id: int, session: Session = Depends(get_session)
):
    return await crud_use_item(
        session, player_id, reward_id
    )  # return type not yet implemented


@router.post("/equip/item/{item_id}", response_model=UseItemResponse)
async def equip_item(item_id: int, slot: str, session: Session = Depends(get_session)):
    return await crud_equip_item(
        session, item_id, slot
    )  # return type not yet implemented


@router.post("/unequip/{item_id}", response_model=UseItemResponse)
async def unequip_item(item_id: int, session: Session = Depends(get_session)):
    return await crud_unequip_item(session, item_id)  # return type not yet implemented


@router.post("/equip/skin/{profile_id}", response_model=UseItemResponse)
async def equip_skin(
    profile_id: int, skin_url: EquipSkinRequest, session: Session = Depends(get_session)
):
    return await crud_equip_skin(profile_id, skin_url, session)


@router.post("/unequip/skin/{profile_id}", response_model=UseItemResponse)
async def unequip_skin(profile_id: int, session: Session = Depends(get_session)):
    return await crud_unequip_skin(profile_id, session)
