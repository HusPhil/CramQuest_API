import random
from sqlmodel import select, desc
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.boss_battle_status_model import BossBattleStatus
from app.models.player_inventory_item_model import EquippedSlot, PlayerInventoryItem
from app.models.reward_model import Reward, RewardType
from app.schemas.boss_battle_status_schema import (
    BossBattleEndRead,
    BossBattlEndInfo,
    BossBattleStatusRead,
)
from app.exceptions.player_exceptions import (
    PlayerNotFound,
)
from app.schemas.reward_schema import RewardRead
from app.services.game_service import RARITY_XP, GameService


async def crud_read_player_boss_battle_statuses(
    session: AsyncSession, player_id: int
) -> List[BossBattleStatusRead]:
    boss_statuses = await _get_boss_battle_statuses_or_error(session, player_id)
    return [_serialize_boss_battle_status(status) for status in boss_statuses]


async def crud_read_player_boss_battle_status(
    session: AsyncSession, status_id: int
) -> BossBattleStatusRead:
    status = await _get_boss_battle_status_or_error(session, status_id)
    return _serialize_boss_battle_status(status)


async def crud_read_player_latest_boss_battle_status(
    player_id: int, session: AsyncSession
) -> BossBattleStatusRead:
    statement = (
        select(BossBattleStatus)
        .where(BossBattleStatus.player_id == player_id)
        .order_by(desc(BossBattleStatus.available_at))
        .limit(1)
    )
    result = await session.execute(statement)
    latest_status = result.scalar_one_or_none()

    if not latest_status:
        raise PlayerNotFound(player_id)

    return _serialize_boss_battle_status(latest_status)


async def crud_end_boss_battle(
    player_id: int, battle_info: BossBattlEndInfo, session: AsyncSession
) -> BossBattleEndRead:
    total_rounds = battle_info.total_rounds
    player_health = battle_info.player_health
    enemy_health = battle_info.enemy_health
    victory = battle_info.victory

    BASE_DROP = 0.05
    ROUND_BONUS = min(total_rounds * 0.01, 0.30)
    HEALTH_BONUS = min(player_health / 1000, 0.15)
    final_drop_chance = min(BASE_DROP + ROUND_BONUS + HEALTH_BONUS, 0.80)

    base_xp = 50
    bonus_xp = 0
    reward_item = None

    if victory:
        ### ✅ 1) Check if player has *any* skin already
        existing_skin = await session.execute(
            select(PlayerInventoryItem)
            .join(Reward)
            .where(
                PlayerInventoryItem.player_id == player_id,
                Reward.type == RewardType.SKIN,
            )
        )
        has_any_skin = existing_skin.scalar_one_or_none()

        if not has_any_skin:
            ### ✅ 2) First ever → force default_1 → skip random roll
            default_skin = await session.execute(
                select(Reward).where(
                    Reward.name == "armored_knight_wood",
                    Reward.type == RewardType.SKIN,
                )
            )
            default_skin = default_skin.scalar_one_or_none()

            if default_skin:
                inv = PlayerInventoryItem(
                    player_id=player_id,
                    reward_id=default_skin.id,
                    quantity=1,
                    equipped_slot=EquippedSlot.SKIN,
                )
                session.add(inv)
                reward_item = default_skin

        else:
            ### ✅ 3) Already has skin → normal drop logic applies
            roll = random.random()
            if roll < final_drop_chance:
                all_items = (await session.execute(select(Reward))).scalars().all()
                if all_items:
                    chosen_item: Reward = GameService.pick_random_item_weighted(
                        all_items
                    )

                    existing = await session.execute(
                        select(PlayerInventoryItem).where(
                            PlayerInventoryItem.player_id == player_id,
                            PlayerInventoryItem.reward_id == chosen_item.id,
                        )
                    )
                    existing_item = existing.scalar_one_or_none()

                    if existing_item:
                        bonus_xp += RARITY_XP[chosen_item.rarity]
                    else:
                        inv = PlayerInventoryItem(
                            player_id=player_id,
                            reward_id=chosen_item.id,
                            quantity=1,
                            equipped_slot=(
                                EquippedSlot.SKIN
                                if chosen_item.type == RewardType.SKIN
                                else None
                            ),
                        )
                        session.add(inv)
                        reward_item = chosen_item

    else:
        enemy_damage_taken = 1 - (enemy_health / 1000)
        bonus_xp += int(enemy_damage_taken * 50)

    await session.commit()

    return BossBattleEndRead(
        base_xp=base_xp,
        bonus_xp=bonus_xp,
        reward_item=(
            RewardRead(
                description=reward_item.description,
                equipped_image_url=reward_item.equipped_image_url,
                image_url=reward_item.image_url,
                id=reward_item.id,
                name=reward_item.name,
                rarity=reward_item.rarity,
                stackable=reward_item.stackable,
                type=reward_item.type,
            )
            if reward_item
            else None
        ),
    )


async def _get_boss_battle_status_or_error(
    session: AsyncSession, status_id: int
) -> BossBattleStatus:
    statement = select(BossBattleStatus).where(BossBattleStatus.id == status_id)
    result = await session.execute(statement)
    status = result.scalar_one_or_none()
    if not status:
        raise PlayerNotFound(-1)
    return status


async def _get_boss_battle_statuses_or_error(
    session: AsyncSession, player_id: int
) -> List[BossBattleStatus]:
    statement = select(BossBattleStatus).where(BossBattleStatus.player_id == player_id)
    result = await session.execute(statement)
    statuses = result.scalars().all()

    if not statuses:
        raise PlayerNotFound(player_id)

    return statuses


def _serialize_boss_battle_status(status: BossBattleStatus) -> BossBattleStatusRead:
    return BossBattleStatusRead(
        id=status.id,
        player_id=status.player_id,
        status=status.status,
        available_at=status.available_at,
        defeated_at=status.defeated_at,
    )
