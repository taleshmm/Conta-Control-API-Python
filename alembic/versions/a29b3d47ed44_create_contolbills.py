"""Create ContolBills

Revision ID: a29b3d47ed44
Revises: 5b3acb3912b9
Create Date: 2024-02-19 20:30:53.473005

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a29b3d47ed44'
down_revision: Union[str, None] = '5b3acb3912b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('controlBills',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=True),
    sa.Column('type_account', sa.String(), nullable=True),
    sa.Column('name_account', sa.String(), nullable=True),
    sa.Column('value_total', sa.Numeric(), nullable=True),
    sa.Column('installments', sa.Integer(), nullable=True),
    sa.Column('value_installments', sa.Numeric(), nullable=True),
    sa.Column('date_buy', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('controlBills')
    # ### end Alembic commands ###