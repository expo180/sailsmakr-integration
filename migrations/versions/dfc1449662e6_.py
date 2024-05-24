"""empty message

Revision ID: dfc1449662e6
Revises: 2fcd9b845491
Create Date: 2024-05-18 15:39:51.312585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfc1449662e6'
down_revision = '2fcd9b845491'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('report', sa.Text(), nullable=True))
        batch_op.drop_column('statsus')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('statsus', sa.VARCHAR(), nullable=False))
        batch_op.drop_column('report')
        batch_op.drop_column('status')

    # ### end Alembic commands ###
