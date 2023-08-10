from pathlib import Path
import os
import shutil

from app.modules.products.tasks import resize_color_icon
from app.db.postgresql.crud import Table

from fastapi import UploadFile


def create_dirs_if_not_exists(path: Path) -> str:
    if not path.parent.exists():
        os.makedirs(path.parent)

    return str(path)


def download_file(name: str, file: UploadFile, model: Table) -> str:
    """Method for creating packages and copying files"""
    name = "_".join(name.lower().split(" "))
    path = create_dirs_if_not_exists(
        Path(
            os.path.join(
                "app", "static", "images", model.__tablename__, name, f"{name}.webp"
            )
        )
    )

    with open(path, "wb+") as file_obj:
        shutil.copyfileobj(file.file, file_obj)
    return str(path)
