from uuid import UUID
from typing import List

from app.db.postgresql.decorators import transaction, duplicate
from app.modules.products.crud.base import BrandCRUD
from .schemas import BrandCreate, BrandDelete, BrandUpdate
from app.modules.products.crud.models import Brand


class BrandService:
    def __init__(self, session):
        self.session = session
        self.brand = BrandCRUD(session=self.session)

    @duplicate("Brand already exists")
    @transaction
    async def create(self, schema: BrandCreate, _commit: bool = True) -> "Brand":
        return await self.brand.insert(data=schema.dict())

    @transaction
    async def update(self, schema: BrandUpdate, _commit: bool = True) -> "Brand":
        schema = schema.model_dump(exclude_none=True)
        uuid = schema.pop("uuid")
        return await self.brand.update(id_=uuid, data=schema)

    async def get(self, id_: UUID) -> "Brand":
        return await self.brand.get(id_=id_)

    async def get_all(self) -> List["Brand"]:
        return await self.brand.select()

    @transaction
    async def delete(self, schema: BrandDelete, _commit: bool = True, **kwargs) -> bool:
        return await self.brand.delete(**schema.dict())
