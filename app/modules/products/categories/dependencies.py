from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.external.s3.dependencies import get_s3
from app.external.s3.service import S3_Service
from app.modules.products.categories.service import CategoryService
from app.modules.products.categories.crud.base import CategoryCRUD
from app.modules.products.categories.crud.models import Category
from app.db.postgresql.dependencies import get_async_session
from .service import CategoryService


def get_category_service(
    session: "AsyncSession" = Depends(get_async_session),
    s3: "S3_Service" = Depends(get_s3),
) -> CategoryService:
    return CategoryService(session=session, crud=CategoryCRUD[Category], s3=s3)
