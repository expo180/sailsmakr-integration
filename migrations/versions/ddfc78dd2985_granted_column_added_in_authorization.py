"""granted column added in Authorization

Revision ID: ddfc78dd2985
Revises: fc98b4c16832
Create Date: 2024-05-26 10:45:57.626152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddfc78dd2985'
down_revision = 'fc98b4c16832'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('authorizations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('granted', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('authorizations', schema=None) as batch_op:
        batch_op.drop_column('granted')

    # ### end Alembic commands ###
