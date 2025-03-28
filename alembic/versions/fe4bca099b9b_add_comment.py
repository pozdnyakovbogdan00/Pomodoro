"""add comment

Revision ID: fe4bca099b9b
Revises: 24e2d70de2f6
Create Date: 2025-03-26 10:55:03.396553

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe4bca099b9b'
down_revision: Union[str, None] = '24e2d70de2f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('UserProfile', sa.Column('comment', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('UserProfile', 'comment')
    # ### end Alembic commands ###
