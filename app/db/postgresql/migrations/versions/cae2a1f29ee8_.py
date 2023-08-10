"""empty message

Revision ID: cae2a1f29ee8
Revises: 41cd8f347dce
Create Date: 2023-07-25 14:53:11.793345

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "cae2a1f29ee8"
down_revision = "41cd8f347dce"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "brand",
        sa.Column("deleted_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("image", sa.String(length=255), nullable=False),
        sa.Column(
            "uuid",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("uuid", name=op.f("pk__brand")),
        sa.UniqueConstraint("name", name=op.f("uq__brand__name")),
    )
    op.create_index(op.f("ix__brand__uuid"), "brand", ["uuid"], unique=True)
    op.create_table(
        "category",
        sa.Column("deleted_at", sa.TIMESTAMP(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("image", sa.String(length=255), nullable=False),
        sa.Column(
            "uuid",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("uuid", name=op.f("pk__category")),
        sa.UniqueConstraint("name", name=op.f("uq__category__name")),
    )
    op.create_index(op.f("ix__category__uuid"), "category", ["uuid"], unique=True)
    op.create_table(
        "color",
        sa.Column("deleted_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("image", sa.String(length=255), nullable=False),
        sa.Column(
            "uuid",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("uuid", name=op.f("pk__color")),
        sa.UniqueConstraint("name", name=op.f("uq__color__name")),
    )
    op.create_index(op.f("ix__color__uuid"), "color", ["uuid"], unique=True)
    op.create_table(
        "collection",
        sa.Column("brand_id", sa.UUID(), nullable=False),
        sa.Column("deleted_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("image", sa.String(length=255), nullable=False),
        sa.Column(
            "uuid",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["brand_id"], ["brand.uuid"], name=op.f("fk__collection__brand_id__brand")
        ),
        sa.PrimaryKeyConstraint("uuid", name=op.f("pk__collection")),
        sa.UniqueConstraint("name", name=op.f("uq__collection__name")),
    )
    op.create_index(op.f("ix__collection__uuid"), "collection", ["uuid"], unique=True)
    op.create_table(
        "model",
        sa.Column("brand_id", sa.UUID(), nullable=False),
        sa.Column("collection_id", sa.UUID(), nullable=False),
        sa.Column("category_id", sa.UUID(), nullable=False),
        sa.Column("box_width", sa.Integer(), nullable=False),
        sa.Column("box_length", sa.Integer(), nullable=False),
        sa.Column("box_height", sa.Integer(), nullable=False),
        sa.Column("box_weight", sa.Integer(), nullable=False),
        sa.Column("open_width", sa.Integer(), nullable=False),
        sa.Column("open_length", sa.Integer(), nullable=False),
        sa.Column("open_height", sa.Integer(), nullable=False),
        sa.Column("close_width", sa.Integer(), nullable=True),
        sa.Column("close_length", sa.Integer(), nullable=True),
        sa.Column("close_height", sa.Integer(), nullable=True),
        sa.Column("weight", sa.Integer(), nullable=False),
        sa.Column(
            "specification", postgresql.JSON(astext_type=sa.Text()), nullable=False
        ),
        sa.Column("deleted_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "uuid",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["brand_id"], ["brand.uuid"], name=op.f("fk__model__brand_id__brand")
        ),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["category.uuid"],
            name=op.f("fk__model__category_id__category"),
        ),
        sa.ForeignKeyConstraint(
            ["collection_id"],
            ["collection.uuid"],
            name=op.f("fk__model__collection_id__collection"),
        ),
        sa.PrimaryKeyConstraint("uuid", name=op.f("pk__model")),
        sa.UniqueConstraint("name", name=op.f("uq__model__name")),
    )
    op.create_index(op.f("ix__model__uuid"), "model", ["uuid"], unique=True)
    op.create_table(
        "product",
        sa.Column("sku", sa.String(length=255), nullable=False),
        sa.Column("price", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column("model_id", sa.UUID(), nullable=False),
        sa.Column("color_id", sa.UUID(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("available", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.TIMESTAMP(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "uuid",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["color_id"], ["color.uuid"], name=op.f("fk__product__color_id__color")
        ),
        sa.ForeignKeyConstraint(
            ["model_id"], ["model.uuid"], name=op.f("fk__product__model_id__model")
        ),
        sa.PrimaryKeyConstraint("uuid", name=op.f("pk__product")),
    )
    op.create_index(op.f("ix__product__sku"), "product", ["sku"], unique=True)
    op.create_index(op.f("ix__product__uuid"), "product", ["uuid"], unique=True)
    op.create_table(
        "product_image",
        sa.Column("path", sa.String(length=255), nullable=False),
        sa.Column("product_id", sa.UUID(), nullable=False),
        sa.Column("deleted_at", sa.TIMESTAMP(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "uuid",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["product.uuid"],
            name=op.f("fk__product_image__product_id__product"),
        ),
        sa.PrimaryKeyConstraint("uuid", name=op.f("pk__product_image")),
    )
    op.create_index(
        op.f("ix__product_image__uuid"), "product_image", ["uuid"], unique=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix__product_image__uuid"), table_name="product_image")
    op.drop_table("product_image")
    op.drop_index(op.f("ix__product__uuid"), table_name="product")
    op.drop_index(op.f("ix__product__sku"), table_name="product")
    op.drop_table("product")
    op.drop_index(op.f("ix__model__uuid"), table_name="model")
    op.drop_table("model")
    op.drop_index(op.f("ix__collection__uuid"), table_name="collection")
    op.drop_table("collection")
    op.drop_index(op.f("ix__color__uuid"), table_name="color")
    op.drop_table("color")
    op.drop_index(op.f("ix__category__uuid"), table_name="category")
    op.drop_table("category")
    op.drop_index(op.f("ix__brand__uuid"), table_name="brand")
    op.drop_table("brand")
    # ### end Alembic commands ###
