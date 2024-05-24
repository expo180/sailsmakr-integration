"""User adress column changed

Revision ID: a5853e584839
Revises: 3df1cd381ead
Create Date: 2024-05-19 11:30:44.998904

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5853e584839'
down_revision = '3df1cd381ead'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address', sa.String(), nullable=True))
        batch_op.drop_column('country')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('country', sa.VARCHAR(), nullable=True))
        batch_op.drop_column('address')

    # ### end Alembic commands ###
