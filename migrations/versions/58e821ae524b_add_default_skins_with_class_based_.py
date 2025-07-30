"""Add default skins with class-based images

Revision ID: 58e821ae524b
Revises: 8837cb4a82a0
Create Date: 2025-07-29 22:29:16.262983

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.models.reward_model import RewardType


# revision identifiers, used by Alembic.
revision: str = "58e821ae524b"
down_revision: Union[str, None] = "8837cb4a82a0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("ALTER TYPE rewardtype ADD VALUE IF NOT EXISTS 'skin';")


def downgrade():
    pass
