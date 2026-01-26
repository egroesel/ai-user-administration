"""migrate existing projects to basic plan

Revision ID: 006_migrate_basic
Revises: 005_plan_provision
Create Date: 2026-01-26

"""
from typing import Sequence, Union
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '006_migrate_basic'
down_revision: Union[str, None] = '005_plan_provision'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Migrate existing projects to basic plan with appropriate provision
    # based on project_type (from pricing.js basic plan values)

    # crowdfunding: 9%
    op.execute("""
        UPDATE projects
        SET plan = 'basic', provision = 9.00
        WHERE plan IS NULL AND project_type = 'crowdfunding'
    """)

    # fundraising: 5%
    op.execute("""
        UPDATE projects
        SET plan = 'basic', provision = 5.00
        WHERE plan IS NULL AND project_type = 'fundraising'
    """)

    # private: 4%
    op.execute("""
        UPDATE projects
        SET plan = 'basic', provision = 4.00
        WHERE plan IS NULL AND project_type = 'private'
    """)


def downgrade() -> None:
    # Remove plan and provision from projects that were migrated
    op.execute("""
        UPDATE projects
        SET plan = NULL, provision = NULL
        WHERE plan = 'basic'
    """)
