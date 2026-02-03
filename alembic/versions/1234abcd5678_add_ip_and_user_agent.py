"""add ip and user agent

Revision ID: 1234abcd5678
Revises: 5a7763cc97bc
Create Date: 2026-02-03 16:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1234abcd5678'
down_revision = '5a7763cc97bc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('transactions', sa.Column('ip_address', sa.String(), nullable=True))
    op.add_column('transactions', sa.Column('user_agent', sa.String(), nullable=True))


def downgrade():
    op.drop_column('transactions', 'user_agent')
    op.drop_column('transactions', 'ip_address')
