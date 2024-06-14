"""password added for Store model

Revision ID: b22e8d717d8e
Revises: 19bb0e91f541
Create Date: 2024-06-13 19:47:53.704352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b22e8d717d8e'
down_revision = '19bb0e91f541'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stores', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stores', schema=None) as batch_op:
        batch_op.drop_column('password')

    # ### end Alembic commands ###
