"""create phone number for user col

Revision ID: ef89fbc9ea7e
Revises: 
Create Date: 2023-08-24 11:28:06.630406

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'ef89fbc9ea7e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # op.alter_column('users', 'phone_number', nullable=True)
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    op.alter_column('users', 'phone_number', nullable=True)
    # op.drop_column('users', 'phone_number')
