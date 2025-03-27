"""edit_access_token_property

Revision ID: 74deb4fd4092
Revises: be1abcd26c8e
Create Date: 2025-03-27 11:34:16.492661

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74deb4fd4092'
down_revision: Union[str, None] = 'be1abcd26c8e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('UserProfile', 'access_token',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('UserProfile', 'access_token',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
