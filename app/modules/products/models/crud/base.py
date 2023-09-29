from app.db.postgresql.crud import CRUD
from app.modules.products.models.crud.models import Model


class ModelCRUD(CRUD[Model]):
    table = Model
