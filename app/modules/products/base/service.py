from typing import List
from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgresql.crud import Table
from app.db.postgresql.decorators import duplicate, transaction
from app.modules.products.utils import download_file
from app.modules.products.tasks.tasks import resize_image
from app.modules.products.base.crud.base import ProductCRUD
from .schemas import ProductCreate, ProductDelete, ProductUpdate


class ProductBaseServiceCRUD:
    duplicate_message = "This entity already exists"

    def __init__(self, session: "AsyncSession", model: Table):
        self.session = session
        self.model = model
        self.entity = ProductCRUD(session=self.session, model=self.model)

    @duplicate(duplicate_message)
    @transaction
    async def create(
        self,
        schema: ProductCreate,
        file: UploadFile,
        _commit: bool = True,
    ) -> Table:
        schema = schema.dict()
        entity = await self.entity.insert(data=schema)
        if file:
            entity.file = download_file(entity.name, file=file, model=self.model)
        return entity

    async def get_all(self, *args, **kwargs) -> List[Table]:
        return await self.entity.select(*args, **kwargs)

    async def get(self, id_: UUID | str) -> Table:
        return await self.entity.get(id_=id_)

    @transaction
    async def update(self, schema, file: UploadFile, _commit: bool = True) -> Table:
        schema = schema.model_dump(exclude_unset=True)
        id_ = schema.pop("uuid")

        if file:
            entity = await self.entity.update(id_=id_, data=schema)
            file = download_file(name=entity.name, file=file, model=self.table)
            entity.file = file
        else:
            entity = await self.entity.update(id_=id_, data=schema)

        return entity

    @transaction
    async def delete(self, schema: ProductDelete, commit: bool = True) -> bool or None:
        return await self.entity.delete(id_=schema.uuid)
