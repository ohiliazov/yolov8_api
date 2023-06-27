"""
Add "model" table

Revision ID: f9e623c9b562
Revises: 91afe2e4b9cd
Create Date: 2023-07-14 09:41:34.545711
"""

import sqlalchemy as sa
from alembic import op

revision = "f9e623c9b562"
down_revision = "91afe2e4b9cd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "model",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("user.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("CREATED", "DOWNLOADING", "VALID", "INVALID", name="ModelStatus"),
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "task_type",
            sa.Enum("DETECT", "SEGMENT", "CLASSIFY", name="TaskType"),
            nullable=False,
        ),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("filename", sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("model")
