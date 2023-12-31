from app.modules.products.base.schemas import (
    ProductCreate,
    ProductDelete,
    ProductRetrieve,
    ProductUpdate,
)


class BrandCreate(ProductCreate):
    ...


class BrandUpdate(ProductUpdate):
    ...


class BrandDelete(ProductDelete):
    ...


class BrandRetrieve(ProductRetrieve):
    ...
