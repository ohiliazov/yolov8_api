"""
Add "project" table

Revision ID: 5ee8535d8c7b
Revises: f9e623c9b562
Create Date: 2023-07-14 09:44:37.447106
"""

import sqlalchemy as sa
from alembic import op

revision = "5ee8535d8c7b"
down_revision = "f9e623c9b562"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "project",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("user.id"), nullable=False),
        sa.Column("model_id", sa.Integer(), sa.ForeignKey("model.id"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("IDLE", "RUNNING", name="projectstatus"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("project")
