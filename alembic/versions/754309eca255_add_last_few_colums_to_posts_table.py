"""add last few colums to posts table

Revision ID: 754309eca255
Revises: b1920410442a
Create Date: 2022-01-03 20:38:41.958694

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '754309eca255'
down_revision = 'b1920410442a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
