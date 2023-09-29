from fastapi import Depends

from app.external.s3.dependencies import get_s3
from app.external.s3.service import S3_Service
from .service import BrandService
from app.db.postgresql.dependencies import get_async_session, AsyncSession
from app.modules.products.brands.crud.base import BrandCRUD


def get_brand_service(
    session: "AsyncSession" = Depends(get_async_session),
    s3: "S3_Service" = Depends(get_s3),
) -> BrandService:
    return BrandService(session=session, s3=s3)
