# app/crud/inventory_crud.py

from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List


from app.models import Reward, PlayerInventoryItem, Profile
from app.models.player_inventory_item_model import EquippedSlot
from app.schemas.player_inventory_item_schema import (
    EquipSkinRequest,
    ItemUses,
    PlayerInventoryItemRead,
    UseItemResponse,
)
from app.schemas.reward_schema import RewardItemRead


async def crud_get_rewards(session: AsyncSession) -> List[RewardItemRead]:
    result = await session.execute(select(Reward))
    return result.scalars().all()


async def crud_get_player_inventory(
    session: AsyncSession, player_id: int
) -> List[PlayerInventoryItemRead]:
    result = await session.execute(
        select(PlayerInventoryItem)
        .where(PlayerInventoryItem.player_id == player_id)
        .options(selectinload(PlayerInventoryItem.reward))
    )

    player_items = [
        PlayerInventoryItemRead(
            id=item.id,
            player_id=item.player_id,
            reward_id=item.reward_id,
            quantity=item.quantity,
            equipped_slot=item.equipped_slot,
            item=RewardItemRead(
                id=item.reward.id,
                name=item.reward.name,
                description=item.reward.description,
                type=item.reward.type,
                rarity=item.reward.rarity,
                stackable=item.reward.stackable,
                equipped_image_url=item.reward.equipped_image_url,
                image_url=item.reward.image_url,
            ),
        )
        for item in result.scalars().all()
    ]
    return player_items


async def crud_get_player_skins(
    session: AsyncSession, player_id: int
) -> List[PlayerInventoryItemRead]:
    result = await session.execute(
        select(PlayerInventoryItem)
        .where(
            (PlayerInventoryItem.player_id == player_id)
            & (PlayerInventoryItem.equipped_slot == EquippedSlot.SKIN)
        )
        .options(selectinload(PlayerInventoryItem.reward))
    )
    player_skins = [
        PlayerInventoryItemRead(
            id=item.id,
            player_id=item.player_id,
            reward_id=item.reward_id,
            quantity=item.quantity,
            equipped_slot=item.equipped_slot,
            item=RewardItemRead(
                id=item.reward.id,
                name=item.reward.name,
                description=item.reward.description,
                type=item.reward.type,
                rarity=item.reward.rarity,
                stackable=item.reward.stackable,
                equipped_image_url=item.reward.equipped_image_url,
                image_url=item.reward.image_url,
            ),
        )
        for item in result.scalars().all()
    ]
    return player_skins


async def crud_check_has_item(
    session: AsyncSession, player_id: int, reward_id: int
) -> bool:
    statement = select(PlayerInventoryItem).where(
        PlayerInventoryItem.player_id == player_id,
        PlayerInventoryItem.reward_id == reward_id,
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none() is not None


async def crud_check_has_quantity(
    session: AsyncSession, player_id: int, reward_id: int, min_quantity: int
) -> bool:
    statement = select(PlayerInventoryItem).where(
        PlayerInventoryItem.player_id == player_id,
        PlayerInventoryItem.reward_id == reward_id,
        PlayerInventoryItem.quantity >= min_quantity,
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none() is not None


async def crud_use_item(session: AsyncSession, player_id: int, reward_id: int) -> None:
    statement = select(PlayerInventoryItem).where(
        PlayerInventoryItem.player_id == player_id,
        PlayerInventoryItem.reward_id == reward_id,
    )
    result = await session.execute(statement)
    item = result.scalar_one_or_none()
    if not item:
        raise Exception("Item not found")

    if item.quantity > 1:
        item.quantity -= 1
    else:
        await session.delete(item)

    await session.commit()


async def crud_equip_item(session: AsyncSession, item_id: int, slot: str) -> None:
    item = await session.get(PlayerInventoryItem, item_id)
    if not item:
        raise Exception("Item not found")

    item.equipped_slot = slot
    await session.commit()


async def crud_equip_skin(
    profile_id: int, skin_equip: EquipSkinRequest, session: AsyncSession
) -> UseItemResponse:
    player_profile = await session.get(Profile, profile_id)
    if not player_profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    player_profile.skin_url = skin_equip.skin_url
    session.add(player_profile)
    await session.commit()
    await session.refresh(player_profile)
    return UseItemResponse(status=ItemUses.EQUIP)


async def crud_unequip_skin(profile_id: int, session: AsyncSession) -> UseItemResponse:
    player_profile = await session.get(Profile, profile_id)
    if not player_profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    player_profile.skin_url = None
    session.add(player_profile)
    await session.commit()
    await session.refresh(player_profile)
    return UseItemResponse(status=ItemUses.UNEQUIP)


async def crud_unequip_item(session: AsyncSession, item_id: int) -> None:
    item = await session.get(PlayerInventoryItem, item_id)
    if not item:
        raise Exception("Item not found")

    item.equipped_slot = None
    await session.commit()
