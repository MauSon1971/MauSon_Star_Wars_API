"""empty message

Revision ID: afb064966382
Revises: c62b57d6c2b4
Create Date: 2024-12-17 22:32:28.808678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'afb064966382'
down_revision = 'c62b57d6c2b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('users_token_key', type_='unique')
        batch_op.drop_column('name')
        batch_op.drop_column('token')
        batch_op.drop_column('age')
        batch_op.drop_column('last_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_name', sa.VARCHAR(length=80), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('age', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('token', sa.VARCHAR(length=250), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=80), autoincrement=False, nullable=False))
        batch_op.create_unique_constraint('users_token_key', ['token'])

    # ### end Alembic commands ###
