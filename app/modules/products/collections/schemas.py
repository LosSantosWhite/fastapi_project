from typing import Optional

from uuid import UUID
from app.modules.products.base.schemas import (
    ProductCreate,
    ProductRetrieve,
    ProductUpdate,
    ProductDelete,
)
from app.modules.products.brands.schemas import BrandRetrieve


class CollectionCreate(ProductCreate):
    brand_id: UUID | str


class CollectionRetrieve(ProductRetrieve):
    brand: BrandRetrieve


class CollectionUpdate(ProductUpdate):
    brand_id: Optional[UUID | str] = None


class CollectionDelete(ProductDelete):
    ...
