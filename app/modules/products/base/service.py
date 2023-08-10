from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgresql.crud import Table
from app.db.postgresql.decorators import duplicate, transaction
from app.modules.products.utils import download_file
from app.modules.products.tasks.tasks import resize_image
from app.modules.products.crud.base import ProductCRUD
from .schemas import ProductCreate, ProductDelete, ProductRetrieve, ProductUpdate


class ProductBaseServiceCRUD:
    duplicate_message = "Entity already exists"

    def __init__(self, session: "AsyncSession", table: Table):
        self.session = session
        self.table = table
        self.entity = ProductCRUD(session=self.session, table=self.table)

    @duplicate(duplicate_message)
    @transaction
    async def create(self, schema: ProductCreate, _commit: bool = True) -> Table:
        entity = await self.entity.insert(data=schema.dict())
        if hasattr(schema, "file"):
            entity.image_path = download_file(
                entity.name, file=schema.file
            )  # TODO: celery?
        return entity

    async def get_all(self, *args, **kwargs) -> Table:
        return await self.entity.select(*args, **kwargs)

    async def get(self, id_: UUID | str) -> Table:
        return await self.entity.get(id_=id_)

    @duplicate(duplicate_message)
    @transaction
    async def update(self, schema: ProductUpdate, _commit: bool = True) -> Table:
        schema = schema.dict()
        id_ = schema.pop("uuid")
        file = schema.pop("file", None)

        if file:
            entity = await self.entity.update(id_=id_, data=schema)
            image_path = download_file(
                name=entity.name, file=file, model=self.table
            )  # TODO: celery?
            entity.image_path = image_path
        else:
            entity = await self.entity.update(id_=id_, data=schema)

        return entity

    @transaction
    async def delete(self, schema: ProductDelete, commit: bool = True) -> bool or None:
        return await self.entity.delete(**schema.dict())
