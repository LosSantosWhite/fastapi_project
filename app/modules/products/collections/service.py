from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgresql.decorators import transaction, duplicate
from app.modules.products.crud.models import Collection
from app.modules.products.crud.base import CollectionCRUD

from .schemas import CollectionCreate


class CollectionService:
    def __init__(self, session: "AsyncSession"):
        self.session = session
        self.collection = CollectionCRUD(session=self.session)

    @duplicate("The collection already exists")
    @transaction
    async def create(
        self, schema: CollectionCreate, _commit: bool = True
    ) -> "Collection":
        return await self.collection.insert(data=schema.dcit())
