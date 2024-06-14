"""new column added for Job Application

Revision ID: 5d37ad7e86bc
Revises: 93f3673879d4
Create Date: 2024-06-13 17:52:32.232519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d37ad7e86bc'
down_revision = '93f3673879d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_applications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_applications', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###