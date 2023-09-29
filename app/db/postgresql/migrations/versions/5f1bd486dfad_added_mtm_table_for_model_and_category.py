"""added mtm table for model and category

Revision ID: 5f1bd486dfad
Revises: 09cf22b8a3c4
Create Date: 2023-09-29 11:57:13.242472

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5f1bd486dfad'
down_revision = '09cf22b8a3c4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('models_categories',
    sa.Column('model_id', sa.UUID(), nullable=True),
    sa.Column('category_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.uuid'], name=op.f('fk__models_categories__category_id__category')),
    sa.ForeignKeyConstraint(['model_id'], ['model.uuid'], name=op.f('fk__models_categories__model_id__model'))
    )
    op.drop_column('model', 'categories_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('model', sa.Column('categories_id', postgresql.ARRAY(sa.UUID()), autoincrement=False, nullable=False))
    op.drop_table('models_categories')
    # ### end Alembic commands ###