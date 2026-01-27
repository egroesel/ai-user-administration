"""add session_id column to ai_drafts for anonymous users

Revision ID: 010_ai_drafts_session
Revises: 009_ai_drafts_plan
Create Date: 2026-01-27

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '010_ai_drafts_session'
down_revision: Union[str, None] = '009_ai_drafts_plan'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add session_id column to ai_drafts for tracking anonymous users
    op.add_column('ai_drafts', sa.Column('session_id', sa.String(255), nullable=True))
    op.create_index('ix_ai_drafts_session_id', 'ai_drafts', ['session_id'])


def downgrade() -> None:
    op.drop_index('ix_ai_drafts_session_id', 'ai_drafts')
    op.drop_column('ai_drafts', 'session_id')
