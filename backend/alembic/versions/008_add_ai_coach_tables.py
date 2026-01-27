"""add AI Coach tables and ai_generated flag

Revision ID: 008_ai_coach
Revises: 007_start_date
Create Date: 2026-01-27

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '008_ai_coach'
down_revision: Union[str, None] = '007_start_date'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add ai_generated and ai_thread_id columns to projects
    op.add_column('projects', sa.Column('ai_generated', sa.Boolean(), nullable=True, server_default='false'))
    op.add_column('projects', sa.Column('ai_thread_id', sa.String(36), nullable=True))

    # Create ai_threads table
    op.create_table(
        'ai_threads',
        sa.Column('id', sa.String(36), primary_key=True, index=True),
        sa.Column('openai_thread_id', sa.String(255), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('session_id', sa.String(255), nullable=True, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Create ai_messages table
    op.create_table(
        'ai_messages',
        sa.Column('id', sa.String(36), primary_key=True, index=True),
        sa.Column('thread_id', sa.String(36), sa.ForeignKey('ai_threads.id', ondelete='CASCADE'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('is_assistant', sa.Boolean(), default=False),
        sa.Column('is_system', sa.Boolean(), default=False),
        sa.Column('token_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Create ai_drafts table
    op.create_table(
        'ai_drafts',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('thread_id', sa.String(36), sa.ForeignKey('ai_threads.id', ondelete='CASCADE'), unique=True, nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('slug', sa.String(255), nullable=True),
        sa.Column('short_description', sa.String(500), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('funding_goal', sa.Numeric(12, 2), nullable=True),
        sa.Column('project_type', sa.String(50), default='crowdfunding'),
        sa.Column('start_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('duration_days', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(50), default='draft'),
        sa.Column('converted_project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('ai_drafts')
    op.drop_table('ai_messages')
    op.drop_table('ai_threads')
    op.drop_column('projects', 'ai_thread_id')
    op.drop_column('projects', 'ai_generated')
