from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.player_model import PlayerTitle


def get_player_initial_next_lvl_xp() -> int:
    from app.services.game_service import GameService

    return GameService.next_level_xp(1)


def determine_player_title(level: int) -> "PlayerTitle":
    """Return the correct PlayerTitle based on level thresholds."""
    from app.models.player_model import PlayerTitle

    if level >= 50:
        return PlayerTitle.OMNISCIENT
    elif level >= 40:
        return PlayerTitle.ARCHMAGE
    elif level >= 30:
        return PlayerTitle.SAGE
    elif level >= 20:
        return PlayerTitle.SCHOLAR
    elif level >= 10:
        return PlayerTitle.ADEPT
    elif level >= 5:
        return PlayerTitle.APPRENTICE
    else:
        return PlayerTitle.NOVICE
