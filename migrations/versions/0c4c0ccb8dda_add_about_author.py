"""add about-author

Revision ID: 0c4c0ccb8dda
Revises: 7ce0cddc05bb
Create Date: 2023-10-20 21:55:13.654013

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c4c0ccb8dda'
down_revision = '7ce0cddc05bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('about_author', sa.Text(length=520), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('about_author')

    # ### end Alembic commands ###
