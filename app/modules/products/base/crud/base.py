from typing import TYPE_CHECKING

from app.db.postgresql.crud import CRUD, Table

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class ProductCRUD(CRUD):
    ...
