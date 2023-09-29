"""init migr

Revision ID: 35ffb602f4b8
Revises: 
Create Date: 2023-09-22 20:41:34.378800

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35ffb602f4b8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('brand',
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.Column('uuid', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk__brand')),
    sa.UniqueConstraint('name', name=op.f('uq__brand__name'))
    )
    op.create_index(op.f('ix__brand__uuid'), 'brand', ['uuid'], unique=True)
    op.create_table('category',
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.Column('uuid', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk__category')),
    sa.UniqueConstraint('name', name=op.f('uq__category__name'))
    )
    op.create_index(op.f('ix__category__uuid'), 'category', ['uuid'], unique=True)
    op.create_table('color',
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.Column('uuid', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk__color')),
    sa.UniqueConstraint('name', name=op.f('uq__color__name'))
    )
    op.create_index(op.f('ix__color__uuid'), 'color', ['uuid'], unique=True)
    op.create_table('collection',
    sa.Column('brand_id', sa.UUID(), nullable=False),
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.Column('uuid', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.ForeignKeyConstraint(['brand_id'], ['brand.uuid'], name=op.f('fk__collection__brand_id__brand')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk__collection')),
    sa.UniqueConstraint('name', name=op.f('uq__collection__name'))
    )
    op.create_index(op.f('ix__collection__uuid'), 'collection', ['uuid'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix__collection__uuid'), table_name='collection')
    op.drop_table('collection')
    op.drop_index(op.f('ix__color__uuid'), table_name='color')
    op.drop_table('color')
    op.drop_index(op.f('ix__category__uuid'), table_name='category')
    op.drop_table('category')
    op.drop_index(op.f('ix__brand__uuid'), table_name='brand')
    op.drop_table('brand')
    # ### end Alembic commands ###
