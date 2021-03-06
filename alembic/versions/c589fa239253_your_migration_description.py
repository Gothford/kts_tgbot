"""your migration description

Revision ID: c589fa239253
Revises: b904fa6a38f9
Create Date: 2021-08-31 04:29:36.665418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c589fa239253'
down_revision = 'b904fa6a38f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('link', sa.Text(), nullable=False),
    sa.Column('link_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user', sa.Column('chat_id', sa.String(length=64), nullable=False))
    op.add_column('user', sa.Column('state', sa.String(length=32), nullable=False))
    op.add_column('user', sa.Column('tags', sa.String(length=32), nullable=True))
    op.add_column('user', sa.Column('timer', sa.String(length=64), nullable=True))
    op.drop_column('user', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.VARCHAR(length=32), autoincrement=False, nullable=False))
    op.drop_column('user', 'timer')
    op.drop_column('user', 'tags')
    op.drop_column('user', 'state')
    op.drop_column('user', 'chat_id')
    op.drop_table('news')
    # ### end Alembic commands ###
