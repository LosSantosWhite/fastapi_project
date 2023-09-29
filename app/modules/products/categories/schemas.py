from typing import Optional

from pydantic import computed_field

from app.modules.products.base.schemas import BaseModelDict


class CategoryBase(BaseModelDict):
    id: int
    name: str
    file: str


class CategoryRetrieve(CategoryBase):
    ...


class CategoryCreate(CategoryBase):
    ...
