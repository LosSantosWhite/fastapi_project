from uuid import UUID
from typing import TYPE_CHECKING

from app.db.postgresql.crud import CRUD, Table
from app.modules.products.crud.models import (
    Brand,
    Category,
    Collection,
    Color,
    Model,
    Sku,
    SkuImage,
)


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class ProductCRUD(CRUD):
    def __init__(self, table: Table):
        self.table = table
