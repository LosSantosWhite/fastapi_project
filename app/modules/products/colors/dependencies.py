from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgresql.dependencies import get_async_session
from app.modules.products.colors.service import ColorService


def get_color_service(
    session: AsyncSession = Depends(get_async_session),
) -> ColorService:
    return ColorService(session=session)
