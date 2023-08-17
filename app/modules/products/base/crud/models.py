from typing import Any, List, Optional
from sqlalchemy import String

from app.db.postgresql.base import Base

from sqlalchemy import ForeignKey
from sqlalchemy.types import DECIMAL
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.db.postgresql.models import Name, ID, Timestamp, Deleted, Image


class Brand(Base, Deleted, Name, Timestamp, Image, ID):
    """
    Table for model's brand
    """

    __tablename__ = "brand"

    collections: Mapped[List["Collection"]] = relationship(
        back_populates="brand", cascade="all, delete-orphan"
    )
    models: Mapped[List["Model"]] = relationship(
        back_populates="brand", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Brand(id={self.uuid}, name={self.name})"


class Collection(Base, Deleted, Name, Timestamp, Image, ID):
    """
    Table for brand's collection
    """

    __tablename__ = "collection"

    brand_id: Mapped[UUID] = mapped_column(
        "brand_id", ForeignKey("brand.uuid"), nullable=False
    )

    brand: Mapped[Brand] = relationship(back_populates="collections")
    models: Mapped[List["Model"]] = relationship(
        back_populates="collection", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Collection(id={self.uuid}, name={self.name})"


class Category(Base, Deleted, Timestamp, Name, Image, ID):
    __tablename__ = "category"

    models: Mapped[List["Model"]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Category(id={self.uuid}, name={self.name})"


class Model(Base, Deleted, Name, Timestamp, ID):
    """
    Table for model of the Sku
    """

    __tablename__ = "model"
    brand_id: Mapped[UUID] = mapped_column(
        "brand_id", ForeignKey("brand.uuid"), nullable=False
    )
    collection_id: Mapped[UUID] = mapped_column(
        "collection_id", ForeignKey("collection.uuid"), nullable=False
    )
    category_id: Mapped[UUID] = mapped_column(
        "category_id", ForeignKey("category.uuid"), nullable=False
    )
    box_width: Mapped[int] = mapped_column("box_width")
    box_length: Mapped[int] = mapped_column("box_length")
    box_height: Mapped[int] = mapped_column("box_height")
    box_weight: Mapped[int] = mapped_column("box_weight")
    open_width: Mapped[int] = mapped_column("open_width")
    open_length: Mapped[int] = mapped_column("open_length")
    open_height: Mapped[int] = mapped_column("open_height")
    close_width: Mapped[Optional[int]] = mapped_column("close_width")
    close_length: Mapped[Optional[int]] = mapped_column("close_length")
    close_height: Mapped[Optional[int]] = mapped_column("close_height")
    weight: Mapped[int] = mapped_column("weight")
    specification: Mapped[dict[str, Any]] = mapped_column("specification", type_=JSON)

    brand: Mapped[Brand] = relationship(back_populates="models")
    collection: Mapped[Collection] = relationship(back_populates="models")
    category: Mapped[Category] = relationship(back_populates="models")

    skus: Mapped[List["Sku"]] = relationship(
        back_populates="model", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Model(name={self.name})"


class Color(Base, Deleted, Name, Timestamp, Image, ID):
    """
    Table for color of the Sku
    """

    __tablename__ = "color"

    skus: Mapped[List["Sku"]] = relationship(
        back_populates="color", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Color(uuid={self.uuid}, name={self.name})"


class Sku(Base, Deleted, Timestamp, ID):
    """
    Table for Sku
    """

    __tablename__ = "sku"

    sku: Mapped[str] = mapped_column(
        "sku", String(255), unique=True, index=True, nullable=False
    )
    price: Mapped[DECIMAL] = mapped_column("price", DECIMAL(10, 2), nullable=False)
    model_id: Mapped[UUID] = mapped_column(
        "model_id", ForeignKey("model.uuid"), nullable=False
    )
    color_id: Mapped[UUID] = mapped_column(
        "color_id", ForeignKey("color.uuid"), nullable=False
    )
    quantity: Mapped[int]
    available: Mapped[bool] = mapped_column("available", default=False)

    model: Mapped[Model] = relationship(back_populates="skus")
    color: Mapped[Color] = relationship(back_populates="skus")

    images: Mapped[List["SkuImage"]] = relationship(
        back_populates="sku", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Sku(id={self.uuid}, price={self.price})"


class SkuImage(Base, Deleted, Timestamp, ID):
    """
    Table for images of the Sku
    """

    __tablename__ = "sku_image"

    path: Mapped[str] = mapped_column("path", String(255))
    sku_id: Mapped[UUID] = mapped_column("sku_id", ForeignKey("sku.uuid"))

    sku: Mapped[Sku] = relationship(back_populates="images")

    def __repr__(self) -> str:
        return f"Image(id={self.uuid}, source={self.source})"
