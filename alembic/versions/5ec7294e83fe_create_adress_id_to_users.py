"""Create Adress Id to Users

Revision ID: 5ec7294e83fe
Revises: dcd90924257d
Create Date: 2023-08-24 13:35:02.572920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '5ec7294e83fe'
down_revision: Union[str, None] = 'dcd90924257d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('USERS', sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key('address_user_fk', source_table="USERS", referent_table="address",
                          local_cols=['address_id'], remote_cols=["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('address_user_fk',table_name="USERS")
    op.drop_column('USERS','address_id')
