"""empty message

Revision ID: d3058ea5363d
Revises: ff5c69f54da9
Create Date: 2025-01-11 02:16:53.882739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3058ea5363d'
down_revision = 'ff5c69f54da9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('interview_status', schema=None) as batch_op:
        batch_op.add_column(sa.Column('interview_id', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('interview_status', schema=None) as batch_op:
        batch_op.drop_column('interview_id')

    # ### end Alembic commands ###
