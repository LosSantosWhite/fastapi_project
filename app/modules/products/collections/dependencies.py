from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgresql.dependencies import get_async_session
from app.modules.products.base.crud.models import Collection
from .service import CollectionService


def get_collection_service(
    session: "AsyncSession" = Depends(get_async_session),
) -> CollectionService:
    return CollectionService(session=session, model=Collection)
