"""new model added for contacts storage

Revision ID: 86832c044e79
Revises: cb8f529a9369
Create Date: 2024-06-20 14:03:00.622928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86832c044e79'
down_revision = 'cb8f529a9369'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('contact', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('last_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('email', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('phone', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('message', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('gender', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('contact', schema=None) as batch_op:
        batch_op.drop_column('gender')
        batch_op.drop_column('message')
        batch_op.drop_column('phone')
        batch_op.drop_column('email')
        batch_op.drop_column('last_name')
        batch_op.drop_column('first_name')

    # ### end Alembic commands ###
