from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "aebd33eb1156"
down_revision: Union[str, None] = "a41ee120274c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add foreign key constraint to weekly_checkin.user_id -> user.id
    op.create_foreign_key(
        constraint_name="fk_weekly_checkin_player_id_player",
        source_table="weeklycheckin",
        referent_table="player",
        local_cols=["player_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        constraint_name="fk_weekly_checkin_player_id_player",
        table_name="weeklycheckin",
        type_="foreignkey",
    )
