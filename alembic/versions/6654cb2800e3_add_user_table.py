"""add user table

Revision ID: 6654cb2800e3
Revises: b66503ba8e54
Create Date: 2022-01-03 20:20:58.087101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6654cb2800e3'
down_revision = 'b66503ba8e54'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False), 
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
