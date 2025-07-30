"""Add default skins with class-based images

Revision ID: 929642f3ab91
Revises: 58e821ae524b
Create Date: 2025-07-29 22:35:43.123731

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "929642f3ab91"
down_revision: Union[str, None] = "58e821ae524b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    connection = op.get_bind()

    skin_groups = {
        "armored_knight": [
            "armored_knight_demonite",
            "armored_knight_gold",
            "armored_knight_hallow",
            "armored_knight_iron",
            "armored_knight_platinum",
            "armored_knight_titanium",
            "armored_knight_wood",
        ],
        "worker": [
            "engineer",
            "police",
            "prince",
        ],
        "default": [
            "default_1",
            "default_2",
            "default_3",
        ],
        "knight": [
            "knight_1",
            "knight_2",
            "knight_3",
            "knight_4",
        ],
    }

    for skin_class, skins in skin_groups.items():
        for skin in skins:
            connection.execute(
                sa.text(
                    """
                    INSERT INTO reward (name, description, type, stackable, image_url, equipped_image_url)
                    VALUES (:name, :description, 'skin', :stackable, :image_url, :equipped_image_url)
                    """
                ),
                {
                    "name": skin,
                    "description": f"Skin: {skin}",
                    "stackable": False,
                    "image_url": f"{skin_class}/{skin}_display.png",
                    "equipped_image_url": f"{skin_class}/{skin}.png",
                },
            )


def downgrade():
    connection = op.get_bind()
    connection.execute(sa.text("DELETE FROM reward WHERE type = 'skin'"))
