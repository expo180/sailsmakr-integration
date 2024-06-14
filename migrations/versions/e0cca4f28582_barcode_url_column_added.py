"""barcode url column added

Revision ID: e0cca4f28582
Revises: d6f5d2a4e72b
Create Date: 2024-06-12 13:30:30.215690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0cca4f28582'
down_revision = 'd6f5d2a4e72b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('purchases', schema=None) as batch_op:
        batch_op.add_column(sa.Column('barcode_url', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('purchases', schema=None) as batch_op:
        batch_op.drop_column('barcode_url')

    # ### end Alembic commands ###
