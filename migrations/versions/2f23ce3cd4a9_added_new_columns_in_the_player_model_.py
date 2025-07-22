"""added new columns in the player model: weekly_streak, longest_weekly_streak, last_checkin_date, last_week_checkin_date

Revision ID: 2f23ce3cd4a9
Revises: 6995b9b6beb3
Create Date: 2025-07-22 22:37:45.836619

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2f23ce3cd4a9"
down_revision: Union[str, None] = "6995b9b6beb3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add columns with default 0 for NOT NULL integer fields
    op.add_column(
        "player",
        sa.Column("weekly_streak", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "player",
        sa.Column(
            "longest_weekly_streak", sa.Integer(), nullable=False, server_default="0"
        ),
    )
    op.add_column("player", sa.Column("last_checkin_date", sa.Date(), nullable=True))
    op.add_column(
        "player", sa.Column("last_week_checkin_date", sa.Date(), nullable=True)
    )

    # Optional: drop server default to enforce explicit inserts in future (safe but not required)
    op.alter_column("player", "weekly_streak", server_default=None)
    op.alter_column("player", "longest_weekly_streak", server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("player", "last_week_checkin_date")
    op.drop_column("player", "last_checkin_date")
    op.drop_column("player", "longest_weekly_streak")
    op.drop_column("player", "weekly_streak")
