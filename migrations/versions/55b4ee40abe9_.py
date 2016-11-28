"""empty message

Revision ID: 55b4ee40abe9
Revises: 
Create Date: 2016-11-25 18:44:58.222000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55b4ee40abe9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.Text(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('u_t_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['u_t_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_tag',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], )
    )
    op.drop_table('page')
    op.drop_table('page_tag')
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)
    op.create_unique_constraint(None, 'user', ['email'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(length=80),
               nullable=True)
    op.create_table('page_tag',
    sa.Column('tag_id', sa.INTEGER(), nullable=True),
    sa.Column('page_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['page_id'], [u'page.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], [u'tag.id'], )
    )
    op.create_table('page',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('url', sa.TEXT(), nullable=False),
    sa.Column('content', sa.TEXT(), nullable=True),
    sa.Column('u_t_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['u_t_id'], [u'user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('post_tag')
    op.drop_table('post')
    ### end Alembic commands ###
