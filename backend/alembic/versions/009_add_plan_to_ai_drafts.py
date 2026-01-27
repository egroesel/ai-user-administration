"""add plan column to ai_drafts

Revision ID: 009_ai_drafts_plan
Revises: 008_ai_coach
Create Date: 2026-01-27

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '009_ai_drafts_plan'
down_revision: Union[str, None] = '008_ai_coach'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add plan column to ai_drafts
    op.add_column('ai_drafts', sa.Column('plan', sa.String(50), nullable=True))


def downgrade() -> None:
    op.drop_column('ai_drafts', 'plan')
