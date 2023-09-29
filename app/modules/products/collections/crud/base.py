from app.db.postgresql.crud import CRUD
from app.modules.products.collections.crud.models import Collection


class CollectionCRUD(CRUD[Collection]):
    ...
