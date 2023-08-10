from fastapi import UploadFile

from app.modules.products.base.schemas.schemas import (
    ProductCreate,
    ProductRetrieve,
    ProductDelete,
    ProductUpdate,
)


class BrandCreate(ProductCreate):
    file: str | UploadFile


class BrandUpdate(ProductUpdate):
    ...


class BrandRetrieve(ProductRetrieve):
    ...


class BrandDelete(ProductDelete):
    ...
