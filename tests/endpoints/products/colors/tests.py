from app.modules.products.base.crud.models import Color
from tests.endpoints.products.base.model import Base


class TestColor(Base[Color]):
    base_url = "/color"
    json_key = "colors"
    model = Color
