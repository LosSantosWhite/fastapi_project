from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.postgresql.base import Base
from app.db.postgresql.models import Deleted, Timestamp, ID

if TYPE_CHECKING:
    from app.modules.products.sku.crud.models import Sku


class SkuImage(Base, Deleted, Timestamp, ID):
    """
    Table for images of the Sku
    """

    __tablename__ = "sku_image"

    path: Mapped[str] = mapped_column("path", String(255))
    sku_id: Mapped[UUID] = mapped_column("sku_id", ForeignKey("sku.uuid"))

    sku: Mapped["Sku"] = relationship(back_populates="images")

    def __repr__(self) -> str:
        return f"Image(id={self.uuid}, source={self.source})"
