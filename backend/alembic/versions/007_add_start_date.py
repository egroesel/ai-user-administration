"""add start_date to projects

Revision ID: 007_start_date
Revises: 006_migrate_basic
Create Date: 2026-01-26

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '007_start_date'
down_revision: Union[str, None] = '006_migrate_basic'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add start_date column to projects table
    op.add_column('projects', sa.Column('start_date', sa.DateTime(timezone=True), nullable=True))

    # Set start_date for already started projects (financing, ended_success, ended_failed)
    # to their created_at date
    op.execute("""
        UPDATE projects
        SET start_date = created_at
        WHERE status IN ('financing', 'ended_success', 'ended_failed')
        AND start_date IS NULL
    """)

    # Set start_date for draft and submitted projects to 2 weeks from now
    op.execute("""
        UPDATE projects
        SET start_date = CURRENT_TIMESTAMP + INTERVAL '14 days'
        WHERE status IN ('draft', 'submitted', 'verified')
        AND start_date IS NULL
    """)


def downgrade() -> None:
    op.drop_column('projects', 'start_date')
