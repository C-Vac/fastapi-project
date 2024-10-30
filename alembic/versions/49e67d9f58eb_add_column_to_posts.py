"""add column to posts

Revision ID: 49e67d9f58eb
Revises: d1b8918a9f44
Create Date: 2024-10-30 08:49:23.292368

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op
from src.database import nuke_database, push_model_updates

# revision identifiers, used by Alembic.
revision: str = "49e67d9f58eb"
down_revision: Union[str, None] = "d1b8918a9f44"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("author_id", sa.Integer(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "author_id")
