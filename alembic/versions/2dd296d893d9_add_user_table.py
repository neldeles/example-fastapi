"""add user table

Revision ID: 2dd296d893d9
Revises: e62792902b0d
Create Date: 2023-09-02 15:24:55.354828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2dd296d893d9"
down_revision = "e62792902b0d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade():
    op.drop_table("users")
