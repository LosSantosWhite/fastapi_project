from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.external.s3.dependencies import get_s3
from app.external.s3.service import S3_Service
from app.db.postgresql.dependencies import get_async_session
from app.modules.products.collections.crud.models import Collection
from app.modules.products.collections.crud.base import CollectionCRUD
from app.modules.products.collections.service import CollectionService


def get_collection_service(
    session: "AsyncSession" = Depends(get_async_session),
    s3: "S3_Service" = Depends(get_s3),
) -> CollectionService:
    return CollectionService(session=session, crud=CollectionCRUD[Collection], s3=s3)
