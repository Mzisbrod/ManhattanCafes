"""Inital migration for cafes table with rating column

Revision ID: 5f1a2bf90b59
Revises: 
Create Date: 2024-11-14 21:51:14.779911

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f1a2bf90b59'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cafes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cafes', schema=None) as batch_op:
        batch_op.drop_column('rating')

    # ### end Alembic commands ###
