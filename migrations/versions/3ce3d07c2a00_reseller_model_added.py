"""reseller model added

Revision ID: 3ce3d07c2a00
Revises: 47d726f7e678
Create Date: 2024-06-11 17:34:46.824340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ce3d07c2a00'
down_revision = '47d726f7e678'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pricing_tags')
    op.drop_table('freights')
    op.drop_table('shippings')
    with op.batch_alter_table('loadings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('unity', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('quantity', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('pricing', sa.Float(), nullable=True))

    with op.batch_alter_table('talks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('content', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('client_email', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('client_phone', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('talks', schema=None) as batch_op:
        batch_op.drop_column('client_phone')
        batch_op.drop_column('client_email')
        batch_op.drop_column('content')
        batch_op.drop_column('title')

    with op.batch_alter_table('loadings', schema=None) as batch_op:
        batch_op.drop_column('pricing')
        batch_op.drop_column('quantity')
        batch_op.drop_column('unity')
        batch_op.drop_column('type')

    op.create_table('shippings',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('freights',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pricing_tags',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
