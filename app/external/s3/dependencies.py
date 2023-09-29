from fastapi import Depends

from app.external.s3.base import get_s3_async_client, get_s3_async_resourse
from app.external.s3.service import S3_Service


async def get_s3(
    client=Depends(get_s3_async_client), resourse=Depends(get_s3_async_resourse)
) -> S3_Service:
    return S3_Service(resource=resourse, client=client)
