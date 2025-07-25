"""rename field in incidentUpdate model

Revision ID: ac1db52ea475
Revises: 571b2e3b603f
Create Date: 2025-07-20 13:21:35.826470

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ac1db52ea475"
down_revision: Union[str, None] = "571b2e3b603f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "incident_updates", sa.Column("description", sa.Text(), nullable=False)
    )
    op.drop_column("incident_updates", "message")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "incident_updates",
        sa.Column("message", sa.TEXT(), autoincrement=False, nullable=False),
    )
    op.drop_column("incident_updates", "description")
    # ### end Alembic commands ###
