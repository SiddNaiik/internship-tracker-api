"""Make application status an enum

Revision ID: 8f921c49f88c
Revises: 82589c5bfc72
Create Date: 2026-06-01 19:56:23.651175

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f921c49f88c'
down_revision: Union[str, Sequence[str], None] = '82589c5bfc72'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

application_status = sa.Enum(
    "applied",
    "online_assessment",
    "interview",
    "offer",
    "rejected",
    "withdrawn",
    name="application_status",
)

def upgrade() -> None:
    # 1) Create enum type in Postgres
    application_status.create(op.get_bind(), checkfirst=True)

    # 2) If there is any old data, normalize common variants (safe even if table empty)
    op.execute("UPDATE applications SET status = lower(status) WHERE status IS NOT NULL;")
    op.execute("UPDATE applications SET status = 'online_assessment' WHERE status IN ('oa', 'online assessment');")

    # 3) Convert column type with explicit cast
    op.execute(
        """
        ALTER TABLE applications
        ALTER COLUMN status TYPE application_status
        USING status::application_status
        """
    )

def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE applications
        ALTER COLUMN status TYPE VARCHAR(50)
        USING status::text
        """
    )
    application_status.drop(op.get_bind(), checkfirst=True)