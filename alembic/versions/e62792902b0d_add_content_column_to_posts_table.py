"""add content column to posts table

Revision ID: e62792902b0d
Revises: f27b16a220d5
Create Date: 2023-09-02 15:05:21.463543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e62792902b0d"
down_revision = "f27b16a220d5"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade():
    op.drop_column("posts", "content")
