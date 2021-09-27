"""your migration description

Revision ID: cd250661a3f0
Revises: da9700c73252
Create Date: 2021-09-01 02:17:35.770641

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd250661a3f0'
down_revision = 'da9700c73252'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sended_news', sa.Column('tag', sa.Text(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sended_news', 'tag')
    # ### end Alembic commands ###