"""empty message

Revision ID: a019bac2609b
Revises: 48a0541a348e
Create Date: 2025-01-09 00:42:46.631379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a019bac2609b'
down_revision = '48a0541a348e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('requirements', schema=None) as batch_op:
        batch_op.alter_column('job_description',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=1000),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('requirements', schema=None) as batch_op:
        batch_op.alter_column('job_description',
               existing_type=sa.String(length=1000),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###