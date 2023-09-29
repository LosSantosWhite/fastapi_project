from typing import List, TYPE_CHECKING

from sqlalchemy import DECIMAL, ForeignKey, UUID, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.postgresql.base import Base
from app.db.postgresql.models import Deleted, Timestamp, ID
from app.modules.products.models.crud.models import Model

from app.modules.products.images.crud.models import SkuImage

if TYPE_CHECKING:
    from app.modules.products.colors.crud.models import Color


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
    quantity: Mapped[int] = mapped_column("quantity", default=0)
    available: Mapped[bool] = mapped_column("available", default=False)

    model: Mapped["Model"] = relationship(back_populates="skus")
    color: Mapped["Color"] = relationship(back_populates="skus")

    images: Mapped[List["SkuImage"]] = relationship(
        back_populates="sku", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Sku(id={self.uuid}, price={self.price})"
