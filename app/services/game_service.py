from datetime import datetime, timezone

from requests import session
from app.models.study_session_model import SessionStatus
from app.models import Player, StudySession, Quest
from sqlmodel import Session


class GameService:
    BASE_XP = 100  # Minimum XP needed for level-up
    INCREMENT = 50  # Small bonus per level
    MULTIPLIER = 20  # Controls exponential growth
    COMPLETION_BONUS = 30  # Extra XP for completing a session
    DEFEAT_PENALTY = 0.5  # Reduce XP by 50% if Defeat
    CANCELED_PENALTY = 0  # No XP for Canceled session

    @staticmethod
    def calculate_xp(
        study_session: StudySession,
        accomplished_quest: Quest,
        total_assigned_tasks: int,
        actual_complete_time: datetime,
        session_status: SessionStatus,
    ) -> int:
        """Calculate XP based on accomplished quests and session result."""

        # ✅ Get session duration in minutes
        duration_minutes = (
            actual_complete_time - study_session.start_time
        ).total_seconds() / 60

        # 1. Get total allotted time
        user_allocated_minutes = (
            study_session.end_time - study_session.start_time
        ).total_seconds() / 60

        # 2. Compute per-task expected time based on total assigned tasks
        # We assume the user evenly distributes time across tasks
        # But we scale it if the quest difficulty is high (to be fair)
        difficulty_factor = 1 + (
            accomplished_quest.difficulty * 0.1
        )  # e.g., difficulty 3 → 1.3x

        per_task_expected_minutes = (
            user_allocated_minutes / total_assigned_tasks
        ) * difficulty_factor

        expected_duration_minutes = per_task_expected_minutes * total_assigned_tasks

        # ✅ Base XP from accomplished quest difficulty
        base_xp = GameService.BASE_XP + (accomplished_quest.difficulty * 5)

        # ✅ Efficiency bonus if finished faster
        efficiency_bonus = (
            GameService.COMPLETION_BONUS
            if duration_minutes < expected_duration_minutes
            else 0
        )

        # ✅ Apply XP multipliers based on outcome
        if session_status == SessionStatus.COMPLETED:
            xp_earned = base_xp + efficiency_bonus  # Full XP
        elif session_status == SessionStatus.DEFEAT:
            xp_earned = int(base_xp * GameService.DEFEAT_PENALTY)  # Reduced XP
        else:
            xp_earned = GameService.CANCELED_PENALTY  # No XP

        return max(xp_earned, 0)  # Ensure XP is never negative

    @staticmethod
    def next_level_xp(level: int) -> int:
        """Calculate XP required to reach the next level."""
        return int(
            GameService.BASE_XP
            + (level * GameService.INCREMENT)
            + (level**1.5 * GameService.MULTIPLIER)
        )
