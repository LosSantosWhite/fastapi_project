from app.modules.products.base.schemas import (
    ProductCreate,
    ProductDelete,
    ProductRetrieve,
    ProductUpdate,
)


class ColorCreate(ProductCreate):
    ...


class ColorUpdate(ProductUpdate):
    ...


class ColorDelete(ProductDelete):
    ...


class ColorRetrieve(ProductRetrieve):
    ...
