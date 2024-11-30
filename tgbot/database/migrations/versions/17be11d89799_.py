"""empty message

Revision ID: 17be11d89799
Revises: 
Create Date: 2024-11-30 20:32:18.978037

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17be11d89799'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_tg_id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('user_tg_id'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('user_tg_id')
    )
    op.create_table('forms',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('latitude', sa.String(), nullable=False),
    sa.Column('longitude', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('price', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_tg_id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('forms')
    op.drop_table('users')
    # ### end Alembic commands ###
