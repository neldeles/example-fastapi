"""add last few columns to posts table

Revision ID: 39eacf422e58
Revises: f6edbe71532f
Create Date: 2023-09-02 15:42:09.790826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "39eacf422e58"
down_revision = "f6edbe71532f"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
