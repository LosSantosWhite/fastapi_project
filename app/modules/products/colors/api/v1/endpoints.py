from typing import List, Union
from uuid import UUID

from fastapi import APIRouter, Depends, status, UploadFile
from app.modules.products.colors.dependencies import get_color_service

from app.modules.products.colors.service import ColorService
from app.modules.products.crud.models import Color
from app.modules.products.colors.schemas import (
    ColorCreate,
    ColorDelete,
    ColorRetrieve,
    ColorUpdate,
)
from app.modules.products.tasks.tasks import resize_color_icon
from app.modules.products.utils import download_file


admin_colors_router = APIRouter(
    prefix="/color", tags=["CRUD operations for product's color model"]
)


@admin_colors_router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=ColorRetrieve
)
async def create_color_as_staff(
    name: str,
    file: UploadFile,
    color_service: ColorService = Depends(get_color_service),
):
    image_path = download_file(name=name, file=file, model=Color)
    color = ColorCreate(name=name, image_path=image_path)
    resize_color_icon.delay(color.image_path, color.name)
    return await color_service.create(schema=color)


@admin_colors_router.get(
    "/all", response_model=List[ColorRetrieve], status_code=status.HTTP_200_OK
)
async def get_all_colors_as_staff(
    color_service: ColorService = Depends(get_color_service),
):
    return await color_service.get_all()


@admin_colors_router.get(
    "/{color_uuid}",
    response_model=Union[ColorRetrieve, None],
    status_code=status.HTTP_200_OK,
)
async def get_color_as_staff(
    color_uuid: UUID | str,
    color_service: ColorService = Depends(get_color_service),
):
    return await color_service.get(id_=color_uuid)


@admin_colors_router.patch("/{color_uuid}", response_model=ColorRetrieve)
async def patch_color_as_staff(
    color_uuid: UUID | str,
    name: str = None,
    image_path: UploadFile = None,
    color_service: ColorService = Depends(get_color_service),
):
    if not name:
        color = await color_service.get(id_=color_uuid)
        name = color.name
    if image_path:
        image_path = download_file(name=name, file=image_path, model=Color)
    schema = ColorUpdate(uuid=color_uuid, name=name, image_path=image_path)
    return await color_service.update(schema=schema)
