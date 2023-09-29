from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgresql.dependencies import get_async_session
from app.external.s3.dependencies import get_s3
from app.external.s3.service import S3_Service
from app.modules.products.models.crud.base import ModelCRUD
from app.modules.products.models.crud.models import Model

from app.modules.products.models.service import ModelService


def get_model_service(
    session: "AsyncSession" = Depends(get_async_session),
    s3: "S3_Service" = Depends(get_s3),
) -> ModelService:
    return ModelService(session=session, crud=ModelCRUD[Model], s3=s3)
