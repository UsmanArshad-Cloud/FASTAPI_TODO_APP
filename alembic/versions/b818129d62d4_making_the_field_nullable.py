"""Making the Field Nullable

Revision ID: b818129d62d4
Revises: b898822ac88a
Create Date: 2023-08-24 12:51:01.519014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b818129d62d4'
down_revision: Union[str, None] = 'b898822ac88a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('USERS', 'phone_number',server_default="0000")


def downgrade() -> None:
    pass
