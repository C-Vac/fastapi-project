"""nuke the database and start fresh

Revision ID: 1dce2050ec5d
Revises: aa4cc6b38500
Create Date: 2024-10-30 10:59:32.738576

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op
from src.database import nuke_database, push_model_updates

# revision identifiers, used by Alembic.
revision: str = "1dce2050ec5d"
down_revision: Union[str, None] = "aa4cc6b38500"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    nuke_database()
    push_model_updates()


def downgrade() -> None:
    nuke_database()
    print("RIP, there is no going back")
