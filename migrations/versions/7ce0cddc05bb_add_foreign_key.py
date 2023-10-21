"""Add foreign key

Revision ID: 7ce0cddc05bb
Revises: 55839a63bcae
Create Date: 2023-10-18 18:13:29.137524

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7ce0cddc05bb'
down_revision = '55839a63bcae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('poster_FK', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'users', ['poster_FK'], ['id'])
        batch_op.drop_column('author')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author', mysql.VARCHAR(length=255), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('poster_FK')

    # ### end Alembic commands ###
