"""add slug to organizations

Revision ID: 571b2e3b603f
Revises: a2df3027a907
Create Date: 2025-07-19 09:52:53.524899

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "571b2e3b603f"
down_revision: Union[str, None] = "a2df3027a907"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _simple_slugify(name: str) -> str:
    return name.strip().lower().replace(" ", "-")


def upgrade() -> None:
    # Step 1: Add slug column as nullable
    op.add_column(
        "organizations", sa.Column("slug", sa.String(length=100), nullable=True)
    )

    # Step 2: Backfill slugs
    connection = op.get_bind()
    orgs = connection.execute(sa.text("SELECT id, name FROM organizations")).fetchall()

    for org in orgs:
        slug = _simple_slugify(org.name)
        connection.execute(
            sa.text("UPDATE organizations SET slug = :slug WHERE id = :id"),
            {"slug": slug, "id": org.id},
        )

    # Step 3: Set slug as non-nullable
    op.alter_column("organizations", "slug", nullable=False)

    # Step 4: Add index
    op.create_index(
        op.f("ix_organizations_slug"), "organizations", ["slug"], unique=True
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_organizations_slug"), table_name="organizations")
    op.drop_column("organizations", "slug")
