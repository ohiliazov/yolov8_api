"""
Add "sample" table

Revision ID: a7810393033d
Revises: 5ee8535d8c7b
Create Date: 2023-07-14 09:45:56.306919
"""

import sqlalchemy as sa
from alembic import op

revision = "a7810393033d"
down_revision = "5ee8535d8c7b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "sample",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "project_id",
            sa.Integer(),
            sa.ForeignKey("project.id"),
            nullable=False,
        ),
        sa.Column("image_filename", sa.String(), nullable=False),
        sa.Column("prediction_filename", sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("sample")
