# app/crud/inventory_crud.py

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models import Reward, PlayerInventoryItem
from app.schemas.player_inventory_item_schema import PlayerInventoryItemRead
from app.schemas.reward_schema import RewardRead


async def crud_get_rewards(session: AsyncSession) -> List[RewardRead]:
    result = await session.execute(select(Reward))
    return result.scalars().all()


async def crud_get_inventory(
    session: AsyncSession, player_id: int
) -> List[PlayerInventoryItemRead]:
    result = await session.execute(
        select(PlayerInventoryItem).where(PlayerInventoryItem.player_id == player_id)
    )
    return result.scalars().all()


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


async def crud_unequip_item(session: AsyncSession, item_id: int) -> None:
    item = await session.get(PlayerInventoryItem, item_id)
    if not item:
        raise Exception("Item not found")

    item.equipped_slot = None
    await session.commit()
