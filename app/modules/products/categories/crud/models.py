from typing import TYPE_CHECKING, List


from sqlalchemy.orm import Mapped, relationship

from app.db.postgresql.base import Base
from app.db.postgresql.models import Name, ID, Timestamp, Deleted, Image

if TYPE_CHECKING:
    from app.modules.products.models.crud.models import Model


# ????
# TODO: Доделать таблицу категорий
# Изменить зависимости
class Category(Base, Deleted, Timestamp, Name, Image, ID):
    __tablename__ = "category"

    def __repr__(self) -> str:
        return f"Category(id={self.uuid}, name={self.name})"
