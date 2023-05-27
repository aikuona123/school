"""Added QuestionType foreign key

Revision ID: f9220bd35b05
Revises: 9d4523d7d182
Create Date: 2023-05-24 00:40:03.907697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9220bd35b05'
down_revision = '9d4523d7d182'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.add_column(sa.Column('question_type_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('QuestionType', 'question_type', ['question_type_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.drop_constraint('QuestionType', type_='foreignkey')
        batch_op.drop_column('question_type_id')

    # ### end Alembic commands ###