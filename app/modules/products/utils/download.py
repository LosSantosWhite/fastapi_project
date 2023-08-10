import os
from pathlib import Path
import shutil

from fastapi import UploadFile

from app.db.postgresql.crud import Table


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
