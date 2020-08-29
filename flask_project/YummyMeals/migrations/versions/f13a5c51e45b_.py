"""empty message

Revision ID: f13a5c51e45b
Revises: 62de57f8bb08
Create Date: 2020-07-30 16:08:22.949932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f13a5c51e45b'
down_revision = '62de57f8bb08'
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
