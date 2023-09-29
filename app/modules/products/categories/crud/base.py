from app.db.postgresql.crud import CRUD
from app.modules.products.categories.crud.models import Category


class CategoryCRUD(CRUD[Category]):
    table = Category
