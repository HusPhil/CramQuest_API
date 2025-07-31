from datetime import datetime
import random
from typing import TypedDict

from app.external.external import determine_player_title
from app.models.reward_model import Reward, RewardRarity
from app.models.study_session_model import SessionStatus
from app.models import Player, StudySession, Quest

RARITY_WEIGHTS = {
    RewardRarity.COMMON: 80,
    RewardRarity.RARE: 15,
    RewardRarity.EPIC: 4,
    RewardRarity.LEGENDARY: 1,
}

RARITY_XP = {
    RewardRarity.COMMON: 20,
    RewardRarity.RARE: 50,
    RewardRarity.EPIC: 120,
    RewardRarity.LEGENDARY: 500,
}


class XPCalculationResult(TypedDict):
    base_xp: int
    efficiency_bonus: int
    total_xp: int


class GameService:
    BASE_XP = 100  # Base XP for any quest
    INCREMENT = 75  # Per level increment
    MULTIPLIER = 20  # Exponential growth factor
    COMPLETION_BONUS = 30  # Max efficiency bonus
    DEFEAT_PENALTY = 0.5  # XP penalty on defeat
    CANCELED_PENALTY = 0  # XP for canceled session
    DIFFICULTY_TIME_FACTOR = 0.1  # % extra time per difficulty point
    DIFFICULTY_XP_EXPONENT = 1.2  # Controls XP curve
    DIFFICULTY_XP_SCALE = 0.1  # % extra XP per difficulty factor

    @staticmethod
    def calculate_xp(
        study_session: StudySession,
        accomplished_quest: Quest,
        total_assigned_tasks: int,
        actual_complete_time: datetime,
        session_status: SessionStatus,
    ) -> XPCalculationResult:
        """Calculate XP based on accomplished quest and session result."""

        # Actual study time in minutes
        duration_minutes = (
            actual_complete_time - study_session.start_time
        ).total_seconds() / 60

        # User allocated total time in minutes
        user_allocated_minutes = (
            study_session.end_time - study_session.start_time
        ).total_seconds() / 60

        # 1️⃣ Time factor: more time for higher difficulty
        difficulty_time_factor = 1 + (
            accomplished_quest.difficulty * GameService.DIFFICULTY_TIME_FACTOR
        )

        per_task_expected_minutes = (
            user_allocated_minutes / total_assigned_tasks
        ) * difficulty_time_factor

        expected_duration_minutes = per_task_expected_minutes * total_assigned_tasks

        # 2️⃣ Base XP factor: scales with difficulty + allocated time
        difficulty_xp_factor = (
            accomplished_quest.difficulty**GameService.DIFFICULTY_XP_EXPONENT
        )
        time_factor = user_allocated_minutes / 60  # convert to hours
        base_xp = int(
            GameService.BASE_XP
            * (1 + difficulty_xp_factor * GameService.DIFFICULTY_XP_SCALE)
            * time_factor
        )

        # 3️⃣ Efficiency bonus: scales up to COMPLETION_BONUS
        efficiency_ratio = expected_duration_minutes / duration_minutes
        scaled_efficiency = max(min(efficiency_ratio - 1, 1), 0)
        efficiency_bonus = int(GameService.COMPLETION_BONUS * scaled_efficiency)

        # 4️⃣ Total XP depends on session result
        if session_status == SessionStatus.COMPLETED:
            total_xp = base_xp + efficiency_bonus
        elif session_status == SessionStatus.DEFEAT:
            total_xp = int(base_xp * GameService.DEFEAT_PENALTY)
            efficiency_bonus = 0
        else:
            total_xp = GameService.CANCELED_PENALTY
            efficiency_bonus = 0

        return {
            "base_xp": base_xp,
            "efficiency_bonus": efficiency_bonus,
            "total_xp": max(total_xp, 0),
        }

    @staticmethod
    def next_level_xp(level: int) -> int:
        """Calculate XP required to reach the next level."""
        return int(
            GameService.BASE_XP
            + (level * GameService.INCREMENT)
            + (level**1.5 * GameService.MULTIPLIER)
        )

    @staticmethod
    def level_up(player: Player, xp_gained: int) -> Player:
        """
        Add XP to the player and handle multiple level-ups if XP overflows.
        Also updates player title when level crosses thresholds.
        """
        player.experience += xp_gained

        while player.experience >= GameService.next_level_xp(player.level):
            required_xp = GameService.next_level_xp(player.level)
            player.experience -= required_xp
            player.level += 1
            player.title = determine_player_title(player.level)

        player.next_level_xp = GameService.next_level_xp(player.level)

        return player

    @staticmethod
    def update_player_streak(player: Player, session_status: SessionStatus) -> Player:
        """
        Updates the player's winning streak:
        - If session is a win → increment streak
        - If session is a defeat or canceled → reset streak
        - Also update longest streak if needed
        """
        if session_status == SessionStatus.COMPLETED:
            player.session_streak += 1
        else:
            player.session_streak = 0  # defeat or canceled resets it
            player.boss_availability_counter = 0

        # ✅ Update longest streak if current streak is higher
        if player.session_streak > player.longest_session_streak:
            player.longest_session_streak = player.session_streak

        return player

    def pick_random_item_weighted(all_items: list[Reward]) -> Reward:
        weights = [RARITY_WEIGHTS[item.rarity] for item in all_items]
        return random.choices(all_items, weights=weights, k=1)[0]
