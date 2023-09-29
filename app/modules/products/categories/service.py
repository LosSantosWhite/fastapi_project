from sqlalchemy.ext.asyncio import AsyncSession


from app.db.postgresql.crud import CRUD
from app.external.s3.service import S3_Service
from app.modules.products.categories.crud.base import CategoryCRUD
from app.modules.products.base.service import ProductServiceBase


class CategoryService(ProductServiceBase):
    duplicate_message = "Category with this name already exists"

    def __init__(self, session: AsyncSession, s3: S3_Service):
        super().__init__(session, s3)
        self.entity = CategoryCRUD(session=self.session)
