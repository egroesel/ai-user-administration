"""add project_type to projects

Revision ID: 004_project_type
Revises: 003_profile_slug
Create Date: 2026-01-24

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '004_project_type'
down_revision: Union[str, None] = '003_profile_slug'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add project_type column with default 'crowdfunding'
    op.add_column('projects', sa.Column('project_type', sa.String(50), nullable=False, server_default='crowdfunding'))

    # Update existing projects to 'crowdfunding'
    op.execute("UPDATE projects SET project_type = 'crowdfunding' WHERE project_type IS NULL")


def downgrade() -> None:
    op.drop_column('projects', 'project_type')
