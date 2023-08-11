from uuid import UUID
from typing import List
from fastapi import APIRouter, status, UploadFile, Depends

from app.modules.products.base.schemas import (
    ProductCreate,
    ProductDelete,
    ProductRetrieve,
    ProductUpdate,
)
from app.modules.products.colors.dependecies import get_color_service
from app.modules.products.colors.service import ColorService

admin_colors_router = APIRouter(
    prefix="/color", tags=["CRUD operations for product's color model"]
)


@admin_colors_router.get(
    "/all", response_model=List[ProductRetrieve], status_code=status.HTTP_200_OK
)
async def get_all_colors_as_staff(
    color_service: ColorService = Depends(get_color_service),
):
    return await color_service.get_all()


@admin_colors_router.get(
    "/{color_uuid}", response_model=ProductRetrieve, status_code=status.HTTP_200_OK
)
async def get_color_as_staff(
    color_uuid: UUID | str, color_service: ColorService = Depends(get_color_service)
):
    return await color_service.get(color_uuid)


@admin_colors_router.post(
    "", response_model=ProductRetrieve, status_code=status.HTTP_201_CREATED
)
async def create_color_as_staff(
    name: str,
    file: UploadFile,
    color_service: ColorService = Depends(get_color_service),
):
    return await color_service.create(schema=ProductCreate(name=name), file=file)


@admin_colors_router.patch(
    "/{color_uuid}", response_model=ProductRetrieve, status_code=status.HTTP_200_OK
)
async def update_color_as_staff(
    color_uuid: UUID | str = None,
    name: str = None,
    file: UploadFile = None,
    color_service: ColorService = Depends(get_color_service),
):
    return await color_service.update(
        schema=ProductUpdate(uuid=color_uuid, name=name), file=file
    )
