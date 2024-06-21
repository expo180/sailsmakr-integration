"""16:34

Revision ID: cb8f529a9369
Revises: e3e39a432d1a
Create Date: 2024-06-18 16:34:58.544192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb8f529a9369'
down_revision = 'e3e39a432d1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('product_img_url',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('product_img_url',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###