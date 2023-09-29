from fastapi import Depends

from app.external.s3.service import S3_Service
from app.external.s3.dependencies import get_s3
from app.modules.products.colors.service import ColorService
from app.db.postgresql.dependencies import get_async_session, AsyncSession
from app.modules.products.colors.crud.models import Color
from app.db.postgresql.crud import CRUD


def get_color_service(
    session: "AsyncSession" = Depends(get_async_session),
    s3: S3_Service = Depends(get_s3),
) -> ColorService:
    return ColorService(session=session, crud=CRUD[Color], s3=s3)
