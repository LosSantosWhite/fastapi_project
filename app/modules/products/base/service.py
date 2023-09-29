from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.external.s3.service import S3_Service
from app.db.postgresql.crud import Table, CRUD
from app.db.postgresql.decorators import duplicate, transaction


class ProductServiceBase:
    duplicate_message = "This entity already exists"

    def __init__(
        self, session: "AsyncSession", s3: S3_Service, crud: CRUD[Table] = None
    ):
        self.session = session
        self.entity = crud(session=self.session)
        self.s3 = s3

    async def get(self, id_: UUID | str) -> Table:
        return await self.entity.get(id_=id_)

    @duplicate(duplicate_message)
    @transaction
    async def create(
        self,
        data: dict,
        file: UploadFile = None,
        _commit: bool = True,
    ) -> Table:
        entity = await self.entity.insert(data=data)

        if file:
            entity_image_url = await self.s3.upload_file(
                file_uuid=entity.uuid, file=file.file
            )
            entity.file = entity_image_url
        return entity
