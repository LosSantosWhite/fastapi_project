from typing import Generator

from aioboto3 import Session
from types_aiobotocore_s3.client import S3Client
from types_aiobotocore_s3.service_resource import S3ServiceResource

from app.config import config


s3_config = dict(
    service_name=config.s3.service_name,
    region_name=config.s3.region_name,
    endpoint_url=config.s3.endpoint_url,
    aws_access_key_id=config.s3.aws_access_key_id,
    aws_secret_access_key=config.s3.aws_secret_access_key,
)


async def get_s3_async_resourse() -> Generator[S3ServiceResource, None, None]:
    async with Session().resource(**s3_config) as s3_resource:
        yield s3_resource


async def get_s3_async_client() -> Generator[S3Client, None, None]:
    async with Session().client(**s3_config) as s3_client:
        yield s3_client
