from typing import List, TYPE_CHECKING
from sqlalchemy.orm import relationship, Mapped

from app.db.postgresql.base import Base
from app.db.postgresql.models import Name, ID, Timestamp, Deleted, Image

from app.modules.products.sku.crud.models import Sku


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
