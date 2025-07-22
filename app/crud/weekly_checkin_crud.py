from datetime import date, timedelta

from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Player, WeeklyCheckIn
from app.schemas.weekly_checkin_schema import CheckInStatus, WeeklyCheckInRead

day_names = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


async def crud_check_in(player_id: int, session: AsyncSession) -> WeeklyCheckInRead:
    today = date.today()
    today_index = today.weekday()

    week_start = today - timedelta(days=today_index)
    day_column = day_names[today_index]

    # Get or create weekly check-in
    stmt = select(WeeklyCheckIn).where(
        WeeklyCheckIn.player_id == player_id,
        WeeklyCheckIn.week_start_date == week_start,
    )
    result = await session.execute(stmt)
    weekly = result.scalar_one_or_none()

    if weekly:
        setattr(weekly, day_column, True)
    else:
        kwargs = {day_column: True}
        weekly = WeeklyCheckIn(
            player_id=player_id, week_start_date=week_start, **kwargs
        )
        session.add(weekly)

    # Load player and update streaks using helper
    player = await session.get(Player, player_id)
    _update_player_streaks(player, today, week_start)

    await session.commit()

    # Build response
    day_statuses = _get_day_statuses(weekly)

    return WeeklyCheckInRead(
        id=weekly.id,
        player_id=weekly.player_id,
        week_start_date=str(weekly.week_start_date),
        monday=day_statuses["mon"],
        tuesday=day_statuses["tue"],
        wednesday=day_statuses["wed"],
        thursday=day_statuses["thu"],
        friday=day_statuses["fri"],
        saturday=day_statuses["sat"],
        sunday=day_statuses["sun"],
    )


async def crud_get_latest_check_in(
    player_id: int, session: AsyncSession
) -> WeeklyCheckInRead:
    today = date.today()
    week_start = today - timedelta(days=today.weekday())

    statement = select(WeeklyCheckIn).where(
        WeeklyCheckIn.player_id == player_id,
        WeeklyCheckIn.week_start_date == week_start,
    )

    result = await session.execute(statement)
    weekly = result.scalar_one_or_none()

    if not weekly:
        weekly = WeeklyCheckIn(player_id=player_id, week_start_date=week_start)
        session.add(weekly)
        await session.commit()

    # Build response
    day_statuses = _get_day_statuses(weekly)

    return WeeklyCheckInRead(
        id=weekly.id,
        player_id=weekly.player_id,
        week_start_date=str(weekly.week_start_date),
        monday=day_statuses["mon"],
        tuesday=day_statuses["tue"],
        wednesday=day_statuses["wed"],
        thursday=day_statuses["thu"],
        friday=day_statuses["fri"],
        saturday=day_statuses["sat"],
        sunday=day_statuses["sun"],
    )


def _get_day_statuses(weekly: WeeklyCheckIn):
    day_statuses = {}
    for i, day_name in enumerate(day_names):
        day_date = weekly.week_start_date + timedelta(days=i)
        is_future = day_date > date.today()
        is_checked = getattr(weekly, day_name, False)
        day_statuses[day_name] = CheckInStatus(
            is_checked=is_checked, is_future=is_future
        )

    return day_statuses


def _update_player_streaks(player: Player, today: date, week_start: date) -> None:
    """
    Given a player, today, and this week's start date,
    update the daily/weekly streaks, longest streaks, and last check-in markers in-place.
    """

    yesterday = today - timedelta(days=1)
    last_week_start = week_start - timedelta(days=7)

    # DAILY
    if player.last_checkin_date == yesterday:
        player.daily_streak += 1
    else:
        player.daily_streak = 1

    player.longest_daily_streak = max(
        player.longest_daily_streak or 0, player.daily_streak
    )

    # WEEKLY
    if player.last_week_checkin_date == last_week_start:
        player.weekly_streak += 1
    else:
        player.weekly_streak = 1

    player.longest_weekly_streak = max(
        player.longest_weekly_streak or 0, player.weekly_streak
    )

    # Update last check-in dates
    player.last_checkin_date = today
    player.last_week_checkin_date = week_start
