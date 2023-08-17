from uuid import UUID
from typing import List
from fastapi import APIRouter, status, UploadFile, Depends

from app.modules.products.colors.schemas import (
    ColorCreate,
    ColorDelete,
    ColorRetrieve,
    ColorUpdate,
)
from app.modules.products.colors.dependecies import get_color_service
from app.modules.products.colors.service import ColorService

admin_colors_router = APIRouter(
    prefix="/color", tags=["CRUD operations for product's color model"]
)


@admin_colors_router.get(
    "/all", response_model=List[ColorRetrieve], status_code=status.HTTP_200_OK
)
async def get_all_colors_as_staff(
    color_service: ColorService = Depends(get_color_service),
):
    result = await color_service.get_all()
    return result


@admin_colors_router.get(
    "/{color_uuid}", response_model=ColorRetrieve, status_code=status.HTTP_200_OK
)
async def get_color_as_staff(
    color_uuid: UUID | str, color_service: ColorService = Depends(get_color_service)
):
    return await color_service.get(color_uuid)


@admin_colors_router.post(
    "", response_model=ColorRetrieve, status_code=status.HTTP_201_CREATED
)
async def create_color_as_staff(
    name: str,
    file: UploadFile,
    color_service: ColorService = Depends(get_color_service),
):
    return await color_service.create(schema=ColorCreate(name=name), file=file)


@admin_colors_router.patch(
    "/{color_uuid}", response_model=ColorRetrieve, status_code=status.HTTP_200_OK
)
async def update_color_as_staff(
    color_uuid: UUID | str = None,
    name: str = None,
    file: UploadFile = None,
    color_service: ColorService = Depends(get_color_service),
):
    return await color_service.update(
        schema=ColorUpdate(uuid=color_uuid, name=name), file=file
    )


@admin_colors_router.delete("/{color_uuid}")
async def delete_color_as_staff(
    color_uuid: UUID | str,
    color_service: ColorService = Depends(get_color_service),
):
    return {
        "status": await color_service.delete(schema=ColorDelete(uuid=color_uuid)),
        "message": "The color has been deleted!",
    }
