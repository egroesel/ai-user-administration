"""add profile_slug to users

Revision ID: 003_profile_slug
Revises: 002_projects
Create Date: 2026-01-24

"""
from typing import Sequence, Union
import re
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session


# revision identifiers, used by Alembic.
revision: str = '003_profile_slug'
down_revision: Union[str, None] = '002_projects'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def generate_slug(name: str) -> str:
    """Generate a URL-safe slug from a name."""
    if not name:
        return ""
    # Convert to lowercase
    slug = name.lower()
    # Replace umlauts and special chars
    replacements = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
        'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i',
        'ó': 'o', 'ò': 'o', 'ô': 'o', 'õ': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u',
        'ñ': 'n', 'ç': 'c'
    }
    for char, replacement in replacements.items():
        slug = slug.replace(char, replacement)
    # Replace spaces and non-alphanumeric with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug


def upgrade() -> None:
    # First add the column as nullable
    op.add_column('users', sa.Column('profile_slug', sa.String(255), nullable=True))

    # Get connection and generate slugs for existing users
    bind = op.get_bind()
    session = Session(bind=bind)

    # Get all users
    users = session.execute(sa.text("SELECT id, full_name, email FROM users")).fetchall()

    used_slugs = set()
    for user in users:
        user_id, full_name, email = user

        # Generate base slug from full_name or email
        if full_name:
            base_slug = generate_slug(full_name)
        else:
            # Use email prefix as fallback
            base_slug = generate_slug(email.split('@')[0])

        if not base_slug:
            base_slug = f"user-{user_id}"

        # Ensure uniqueness
        slug = base_slug
        counter = 1
        while slug in used_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1

        used_slugs.add(slug)

        # Update user with slug
        session.execute(
            sa.text("UPDATE users SET profile_slug = :slug WHERE id = :id"),
            {"slug": slug, "id": user_id}
        )

    session.commit()

    # Make full_name required (set default for null values first)
    session.execute(
        sa.text("UPDATE users SET full_name = email WHERE full_name IS NULL OR full_name = ''")
    )
    session.commit()

    # Now make profile_slug not nullable and add unique constraint
    op.alter_column('users', 'profile_slug', nullable=False)
    op.create_index('ix_users_profile_slug', 'users', ['profile_slug'], unique=True)

    # Make full_name not nullable
    op.alter_column('users', 'full_name', nullable=False)


def downgrade() -> None:
    op.drop_index('ix_users_profile_slug', table_name='users')
    op.drop_column('users', 'profile_slug')
    op.alter_column('users', 'full_name', nullable=True)
