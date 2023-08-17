from fastapi import Depends


from .service import ColorService
from app.db.postgresql.dependencies import get_async_session, AsyncSession
from app.modules.products.base.crud.models import Color


def get_color_service(
    session: "AsyncSession" = Depends(get_async_session),
) -> ColorService:
    return ColorService(session=session, model=Color)
