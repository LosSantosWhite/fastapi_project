from typing import List, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column


from app.db.postgresql.base import Base
from app.db.postgresql.models import Name, ID, Timestamp, Deleted, Image

if TYPE_CHECKING:
    from app.modules.products.brands.crud.models import Brand
    from app.modules.products.models.crud.models import Model


class Collection(Base, Deleted, Name, Timestamp, Image, ID):
    """
    Table for brand's collection
    """

    __tablename__ = "collection"

    brand_id: Mapped[UUID] = mapped_column(
        "brand_id", ForeignKey("brand.uuid"), nullable=False
    )

    brand: Mapped["Brand"] = relationship(back_populates="collections")
    models: Mapped[List["Model"]] = relationship(
        back_populates="collection", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Collection(id={self.uuid}, name={self.name})"
