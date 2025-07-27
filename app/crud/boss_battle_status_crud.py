from sqlmodel import select, desc
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.boss_battle_status_model import BossBattleStatus
from app.schemas.boss_battle_status_schema import BossBattleStatusRead
from app.exceptions.player_exceptions import (
    PlayerNotFound,
)


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
    session: AsyncSession, player_id: int
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
