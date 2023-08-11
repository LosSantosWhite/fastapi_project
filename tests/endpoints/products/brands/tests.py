from tests.endpoints.products.base.model import Base
from app.modules.products.crud.models import Brand


class TestBrand(Base[Brand]):
    base_url = "/brand"
    model = Brand
    json_key = "brands"
