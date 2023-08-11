from typing import List
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.products.crud.models import Color
from tests.endpoints.products.base.model import Base


class TestColor(Base[Color]):
    base_url = "/color"
    json_key = "colors"
    model = Color
