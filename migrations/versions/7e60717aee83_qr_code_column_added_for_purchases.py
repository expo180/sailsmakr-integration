"""qr code column added for purchases

Revision ID: 7e60717aee83
Revises: 917067e90ff3
Create Date: 2024-05-25 19:36:22.066010

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e60717aee83'
down_revision = '917067e90ff3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('purchases', schema=None) as batch_op:
        batch_op.add_column(sa.Column('qr_code_url', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('purchases', schema=None) as batch_op:
        batch_op.drop_column('qr_code_url')

    # ### end Alembic commands ###
