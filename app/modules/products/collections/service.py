from uuid import UUID

from typing import List
from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.orm import selectinload


from app.modules.products.base.service import ProductBaseServiceCRUD
from app.modules.products.base.crud.models import Brand, Collection
from .schemas import CollectionUpdate


class CollectionService(ProductBaseServiceCRUD):
    update_model = CollectionUpdate

    async def get_all(self) -> List[Collection]:
        stmt = select(Collection).options(selectinload(Collection.brand))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, schema, file, _commit: bool = True):
        entity = await super().create(schema=schema, file=file, _commit=_commit)
        return await self.get(id_=entity.uuid)

    async def get(self, id_: str | UUID) -> Collection:
        stmt = (
            select(Collection)
            .options(selectinload(Collection.brand))
            .where(Collection.uuid == id_)
        )
        result = await self.session.execute(stmt)

        return result.scalar_one()

    async def update(
        self, schema: CollectionUpdate, file: UploadFile = None
    ) -> Collection:
        entity = await super().update(schema=schema, file=file)
        return await self.get(id_=entity.uuid)
