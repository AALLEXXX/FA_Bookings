"""add name in users

Revision ID: c3d71329e036
Revises: 880bcbc76d21
Create Date: 2024-03-04 16:38:27.551752

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c3d71329e036'
down_revision: Union[str, None] = '880bcbc76d21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
