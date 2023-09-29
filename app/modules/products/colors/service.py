from uuid import UUID
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgresql.decorators import transaction, duplicate
from app.modules.products.colors.crud.base import ColorCRUD
from app.modules.products.colors.crud.models import Color
from app.modules.products.colors.schemas import ColorCreate, ColorUpdate
from app.modules.products.base.service import ProductServiceBase


class ColorService(ProductServiceBase):
    duplicate_message = "Color with this name already exists!"
