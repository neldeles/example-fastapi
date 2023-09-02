"""create posts table

Revision ID: f27b16a220d5
Revises: 
Create Date: 2023-09-02 14:06:35.325677

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f27b16a220d5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )


def downgrade():
    op.drop_table("posts")
