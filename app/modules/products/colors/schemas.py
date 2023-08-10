from fastapi import UploadFile

from app.modules.products.base.schemas.schemas import (
    ProductCreate,
    ProductUpdate,
    ProductDelete,
    ProductRetrieve,
)


class ColorCreate(ProductCreate):
    image_path: str
    ...


class ColorUpdate(ProductUpdate):
    ...


class ColorDelete(ProductDelete):
    ...


class ColorRetrieve(ProductRetrieve):
    ...
