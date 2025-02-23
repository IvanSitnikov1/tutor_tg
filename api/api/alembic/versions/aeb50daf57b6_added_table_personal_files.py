"""added table personal_files

Revision ID: aeb50daf57b6
Revises: 47a18ac55547
Create Date: 2025-02-23 19:09:30.068769

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aeb50daf57b6'
down_revision: Union[str, None] = '47a18ac55547'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('personal_files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('file_path', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['teachers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('personal_files')
    # ### end Alembic commands ###
