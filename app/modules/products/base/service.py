from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgresql.crud import Table
from app.db.postgresql.decorators import duplicate, transaction
from app.modules.products.utils import download_file
from app.modules.products.tasks.tasks import resize_color_icon
from app.modules.products.crud.base import ProductCRUD
from .schemas import ProductCreate, ProductDelete, ProductRetrieve, ProductUpdate


class ProductBaseServiceCRUD:
    def __init__(self, session: "AsyncSession", table: Table):
        self.session = session
        self.entity = ProductCRUD(session=self.session, table=table)

    @duplicate(f"Entity already exists")
    @transaction
    async def create(self, schema: ProductCreate, _commit: bool = True) -> Table:
        if hasattr(schema, "file"):
            entity = await self.entity.insert(data=schema.dict())
            entity.image_path = download_file(entity.name, file=schema.file)
        return

    async def get_all(self) -> Table:
        return await self.entity.select()

    async def get(self, id_: UUID | str) -> Table:
        return await self.entity.get(id_=id_)

    @duplicate("Entity already exists")
    @transaction
    async def update(self, schema: dict, _commit: bool = True) -> Table:
        id_ = schema.pop("id")
        if schema.get("file"):
            ...
        return await self.entity.update(id_=id_, data=schema)

    def file_process(self, file: UploadFile):
        ...
