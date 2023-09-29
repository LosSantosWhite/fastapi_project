from typing import Any, List, Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSON, ARRAY, UUID

from app.db.postgresql.base import Base
from app.db.postgresql.models import Name, ID, Timestamp, Deleted
from app.modules.products.categories.crud.models import Category

if TYPE_CHECKING:
    from app.modules.products.brands.crud.models import Brand
    from app.modules.products.collections.crud.models import Collection
    from app.modules.products.images.crud.models import Image
    from app.modules.products.sku.crud.models import Sku

model_category_mtm_table = Table(
    "models_categories",
    Base.metadata,
    Column(
        "model_id",
        ForeignKey("model.uuid"),
    ),
    Column("category_id", ForeignKey("category.uuid")),
)


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

    categories: Mapped[List[UUID]] = relationship(
        "Category", secondary=model_category_mtm_table
    )
    brand: Mapped["Brand"] = relationship(back_populates="models")
    collection: Mapped["Collection"] = relationship(back_populates="models")

    skus: Mapped[List["Sku"]] = relationship(
        back_populates="model", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Model(name={self.name})"
