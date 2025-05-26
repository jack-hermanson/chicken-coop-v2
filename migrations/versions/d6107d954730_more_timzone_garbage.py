"""more_timzone_garbage

Revision ID: d6107d954730
Revises: ec5a9dacf44d
Create Date: 2025-05-26 13:39:06.957459

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d6107d954730"
down_revision = "ec5a9dacf44d"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "account",  # Replace with actual table
        "last_login",
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="last_login AT TIME ZONE 'UTC'",
    )


def downgrade():
    op.alter_column(
        "account",
        "last_login",
        type_=sa.TIMESTAMP(timezone=False),
        postgresql_using="last_login AT TIME ZONE 'UTC'",
    )
