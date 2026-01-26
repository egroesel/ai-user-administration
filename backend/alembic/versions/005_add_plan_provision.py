"""add plan and provision to projects

Revision ID: 005_plan_provision
Revises: 004_project_type
Create Date: 2026-01-26

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '005_plan_provision'
down_revision: Union[str, None] = '004_project_type'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add plan column (basic, pro, premium, enterprise)
    op.add_column('projects', sa.Column('plan', sa.String(50), nullable=True))

    # Add provision column (percentage, e.g. 7.00 for 7%)
    op.add_column('projects', sa.Column('provision', sa.Numeric(5, 2), nullable=True))

    # Add voucher_code column (optional, for tracking applied vouchers)
    op.add_column('projects', sa.Column('voucher_code', sa.String(50), nullable=True))


def downgrade() -> None:
    op.drop_column('projects', 'voucher_code')
    op.drop_column('projects', 'provision')
    op.drop_column('projects', 'plan')
