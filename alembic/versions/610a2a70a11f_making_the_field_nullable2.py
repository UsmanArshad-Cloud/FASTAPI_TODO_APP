"""Making the Field Nullable2

Revision ID: 610a2a70a11f
Revises: b818129d62d4
Create Date: 2023-08-24 13:02:43.152920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '610a2a70a11f'
down_revision: Union[str, None] = 'b818129d62d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sql_query = f"UPDATE public.\"USERS\" SET phone_number = '1234'"
    op.execute(sql_query)
    op.alter_column('USERS', 'phone_number', nullable=False)


def downgrade() -> None:
    pass
