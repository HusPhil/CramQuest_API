"""modified the QuestStus now with to_do, doing, and done

Revision ID: fcef28582bee
Revises: 145f56c89b8a
Create Date: 2025-07-20 08:45:07.830574

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = "fcef28582bee"
down_revision: Union[str, None] = "145f56c89b8a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create a connection to execute raw SQL
    connection = op.get_bind()

    # Update existing records to map old enum values to new ones
    # IN_PROGRESS -> DOING
    connection.execute(
        text("UPDATE quest SET status = 'doing' WHERE status = 'in_progress'")
    )

    # COMPLETED -> DONE
    connection.execute(
        text("UPDATE quest SET status = 'done' WHERE status = 'completed'")
    )

    # If you're using PostgreSQL with actual ENUM types, you might also need:
    # This depends on your database setup - uncomment if using PostgreSQL ENUMs

    # # Add new enum values
    # op.execute("ALTER TYPE queststatus ADD VALUE 'to_do'")
    # op.execute("ALTER TYPE queststatus ADD VALUE 'doing'")
    # op.execute("ALTER TYPE queststatus ADD VALUE 'done'")

    # # Update existing records (already done above)

    # # Remove old enum values (this requires recreating the enum in PostgreSQL)
    # # This is complex with PostgreSQL - consider leaving old values if they're not causing issues


def downgrade() -> None:
    """Downgrade schema."""
    # Create a connection to execute raw SQL
    connection = op.get_bind()

    # Revert the enum value changes
    # DOING -> IN_PROGRESS
    connection.execute(
        text("UPDATE quest SET status = 'in_progress' WHERE status = 'doing'")
    )

    # DONE -> COMPLETED
    connection.execute(
        text("UPDATE quest SET status = 'completed' WHERE status = 'done'")
    )

    # Note: Records with TO_DO status would need to be handled
    # You might want to set them to IN_PROGRESS or handle them specifically
    connection.execute(
        text("UPDATE quest SET status = 'in_progress' WHERE status = 'to_do'")
    )

    # For PostgreSQL ENUM cleanup (if applicable):
    # Similar complex operations would be needed to remove the new enum values
