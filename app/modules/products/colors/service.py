from typing import List, TYPE_CHECKING
from uuid import UUID

from app.modules.products.crud.base import ColorCRUD
from app.db.postgresql.decorators import duplicate, transaction

from .schemas import ColorCreate, ColorUpdate, ColorRetrieve, ColorDelete
from app.modules.products.crud.models import Color

if TYPE_CHECKING:
    from app.db.postgresql.dependencies import AsyncSession


class ColorService:
    def __init__(self, session: "AsyncSession"):
        self.session = session
        self.color = ColorCRUD(session=self.session)

    async def get(self, id_: UUID | str) -> "Color":
        return await self.color.get(id_=id_)

    async def get_all(self) -> List["Color"]:
        return await self.color.select()

    @transaction
    @duplicate("Color already exists")
    async def create(self, schema: ColorCreate, _commit: bool = True) -> "Color":
        return await self.color.insert(schema.dict())

    @transaction
    async def update(self, schema: ColorUpdate, _commit: bool = True) -> "Color":
        schema = schema.model_dump(exclude_none=True)
        uuid = schema.pop("uuid")
        return await self.color.update(id_=uuid, data=schema)

    @transaction
    async def delete(self, color_uuid: ColorDelete) -> True or None:
        return await self.color.delete(color_uuid)
