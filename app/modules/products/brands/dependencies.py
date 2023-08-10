from fastapi import Depends


from .service import BrandService
from app.db.postgresql.dependencies import get_async_session, AsyncSession


def get_brand_service(
    session: "AsyncSession" = Depends(get_async_session),
) -> BrandService:
    return BrandService(session=session)
