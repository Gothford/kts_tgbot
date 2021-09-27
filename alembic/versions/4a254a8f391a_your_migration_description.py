"""your migration description

Revision ID: 4a254a8f391a
Revises: 6bec64274e4a
Create Date: 2021-08-31 04:41:52.786500

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a254a8f391a'
down_revision = '6bec64274e4a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'tags',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
    op.alter_column('user', 'timer',
               existing_type=sa.VARCHAR(length=64),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'timer',
               existing_type=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('user', 'tags',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)
    # ### end Alembic commands ###
