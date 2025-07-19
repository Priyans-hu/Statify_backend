"""add default statuses to status_master

Revision ID: a2df3027a907
Revises: 352fcbf76436
Create Date: 2025-07-19 06:33:51.628382

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a2df3027a907"
down_revision: Union[str, None] = "352fcbf76436"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    statuses = [
        {"id": 1, "status": "Operational"},
        {"id": 2, "status": "Degraded Performance"},
        {"id": 3, "status": "Partial Outage"},
        {"id": 4, "status": "Major Outage"},
    ]

    status_table = sa.table(
        "status_master",
        sa.column("id", sa.Integer),
        sa.column("status", sa.String),
    )

    op.bulk_insert(status_table, statuses)


def downgrade():
    op.execute("DELETE FROM status_master WHERE id IN (1, 2, 3, 4)")
