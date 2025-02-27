"""Added profile picture to influencer model

Revision ID: 98692c4e7fbb
Revises: 40b3af8e2cee
Create Date: 2024-08-07 22:01:53.101389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98692c4e7fbb'
down_revision = '40b3af8e2cee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('influencer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_picture', sa.String(length=300), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('influencer', schema=None) as batch_op:
        batch_op.drop_column('profile_picture')

    # ### end Alembic commands ###
