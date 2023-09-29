from app.db.postgresql.crud import CRUD

from .models import Color


class ColorCRUD(CRUD[Color]):
    ...
