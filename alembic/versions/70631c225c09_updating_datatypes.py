"""Updating DataTypes

Revision ID: 70631c225c09
Revises: 5ec7294e83fe
Create Date: 2023-08-24 18:49:34.849450

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '70631c225c09'
down_revision: Union[str, None] = '5ec7294e83fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('address', 'address1', type_=sa.String(), existing_type=sa.Integer())
    op.alter_column('address', 'address2', type_=sa.String(), existing_type=sa.Integer())
    op.alter_column('address', 'city', type_=sa.String(), existing_type=sa.Integer())
    op.alter_column('address', 'state', type_=sa.String(), existing_type=sa.Integer())
    op.alter_column('address', 'country', type_=sa.String(), existing_type=sa.Integer())
    op.alter_column('address', 'postalcode', type_=sa.String(), existing_type=sa.Integer())


def downgrade() -> None:
    pass
