"""add content column to posts table

Revision ID: b66503ba8e54
Revises: d1da4814ce19
Create Date: 2022-01-03 20:09:28.813329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b66503ba8e54'
down_revision = 'd1da4814ce19'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
