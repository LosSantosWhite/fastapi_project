from typing import List, TYPE_CHECKING

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from app.db.postgresql.base import Base
from app.db.postgresql.models import Name, ID, Timestamp, Deleted, Image

if TYPE_CHECKING:
    from app.modules.products.collections.crud.models import Collection
    from app.modules.products.models.crud.models import Model


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
        return f"<Brand(id={self.uuid}, name={self.name})>"
