"""create posts table

Revision ID: d1b8918a9f44
Revises: 
Create Date: 2024-10-30 08:41:16.203107

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op
from src.database import nuke_database, push_model_updates

# revision identifiers, used by Alembic.
revision: str = "d1b8918a9f44"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("posts")
