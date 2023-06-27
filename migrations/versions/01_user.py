"""
Add "user" table

Revision ID: 91afe2e4b9cd
Revises:
Create Date: 2023-07-14 09:40:49.652234
"""

import sqlalchemy as sa
from alembic import op

revision = "91afe2e4b9cd"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(), unique=True, nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("disabled", sa.Boolean(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("user")
