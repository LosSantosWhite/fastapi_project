from uuid import UUID
from typing import Any
from pydantic import AnyUrl
from aioboto3.session import ResourceCreatorContext
from aioboto3 import Session as boto3_session
from types_aiobotocore_s3.client import S3Client


from app.config import config


class S3_Service:
    bucket_name = config.s3.bucket_name
    endpoint_url = config.s3.endpoint_url

    def __init__(self, resource: boto3_session.resource, client: S3Client):
        self.resource = resource
        self.client = client

    async def upload_file(self, file: bytes, file_uuid: UUID | str) -> str:
        await self.client.put_object(
            Bucket=self.bucket_name,
            Body=file._file,
            Key=str(file_uuid),
            ContentType="image/webp",
        )

        image_url = f"{self.endpoint_url}/{self.bucket_name}/{file_uuid}.webp"
        return image_url
