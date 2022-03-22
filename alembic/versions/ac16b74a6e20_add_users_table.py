"""Add user table

Revision ID: b5f3e3036183
Revises: 9301bd3e86ce
Create Date: 2022-03-12 12:38:24.753957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5f3e3036183'
down_revision = '9301bd3e86ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_post_user', 'posts', 'users', [
                          'user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_post_user', 'posts', type_='foreignkey')
    op.drop_column('posts', 'user_id')
    # ### end Alembic commands ###
