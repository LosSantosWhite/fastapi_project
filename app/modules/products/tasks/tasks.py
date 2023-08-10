from pathlib import Path
import shutil
import os

from fastapi import UploadFile
from PIL import Image

from app.db.postgresql.crud import Table
from .celery import celery


@celery.task
def resize_image(path: str, name: str, heigth: int, width: int, model: Table):
    path = Path(path)
    im = Image.open(path)
    resized_image = im.resize((heigth, width))
    resized_image.save(f"./app/static/images/{model.__tablename__}/{name}/{name}.webp")
