"""empty message

Revision ID: e042c0e1b502
Revises: cc596af65c1c
Create Date: 2025-01-12 14:22:34.292980

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e042c0e1b502'
down_revision = 'cc596af65c1c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('interview_status', schema=None) as batch_op:
        batch_op.add_column(sa.Column('candidate_name', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('interviewer_name', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('interview_date', sa.DateTime(), nullable=True))
        batch_op.alter_column('interview_id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('interview_status', schema=None) as batch_op:
        batch_op.alter_column('interview_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
        batch_op.drop_column('interview_date')
        batch_op.drop_column('interviewer_name')
        batch_op.drop_column('candidate_name')

    # ### end Alembic commands ###
