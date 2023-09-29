from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgresql.crud import CRUD
from app.external.s3.service import S3_Service
from app.modules.products.base.service import ProductServiceBase
from app.modules.products.brands.crud.base import BrandCRUD


class BrandService(ProductServiceBase):
    duplicate_message = "Brand already exists"

    def __init__(self, session: AsyncSession, s3: S3_Service):
        super().__init__(session, s3)
        self.entity = BrandCRUD(session=self.session)
