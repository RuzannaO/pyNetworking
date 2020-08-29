"""empty message

Revision ID: c26903381782
Revises: f13a5c51e45b
Create Date: 2020-07-30 16:08:58.965368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c26903381782'
down_revision = 'f13a5c51e45b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_admin', sa.Boolean(), nullable=False))
    op.drop_constraint(None, 'user__favorite', type_='foreignkey')
    op.create_foreign_key(None, 'user__favorite',
                          'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'user_comments', type_='foreignkey')
    op.create_foreign_key(
        None, 'user_comments', 'meal', ['meal_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_comments', type_='foreignkey')
    op.create_foreign_key(None, 'user_comments', 'meal', ['meal_id'], ['id'])
    op.drop_constraint(None, 'user__favorite', type_='foreignkey')
    op.create_foreign_key(None, 'user__favorite', 'user', ['user_id'], ['id'])
    op.drop_column('user', 'is_admin')
    # ### end Alembic commands ###
