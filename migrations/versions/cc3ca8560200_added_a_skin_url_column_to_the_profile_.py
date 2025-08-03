"""added a skin_url column to the profile model for equip and unequip of skins

Revision ID: cc3ca8560200
Revises: 1325bed56a31
Create Date: 2025-08-03 18:23:43.216282

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cc3ca8560200"
down_revision: Union[str, None] = "1325bed56a31"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "profile", sa.Column("skin_url", sa.String(length=255), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("profile", "skin_url")
