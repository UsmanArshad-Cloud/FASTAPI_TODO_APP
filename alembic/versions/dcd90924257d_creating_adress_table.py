"""Creating Adress Table

Revision ID: dcd90924257d
Revises: 610a2a70a11f
Create Date: 2023-08-24 13:21:41.367689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'dcd90924257d'
down_revision: Union[str, None] = '610a2a70a11f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('address',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('address1', sa.Integer(), nullable=False),
                    sa.Column('address2', sa.Integer(), nullable=False),
                    sa.Column('city', sa.Integer(), nullable=False),
                    sa.Column('state', sa.Integer(), nullable=False),
                    sa.Column('country', sa.Integer(), nullable=False),
                    sa.Column('postalcode', sa.Integer(), nullable=False)
                    )


def downgrade() -> None:
    op.drop_table('address')
