from app.db.postgresql.crud import CRUD
from app.modules.products.brands.crud.models import Brand


class BrandCRUD(CRUD[Brand]):
    table = Brand
