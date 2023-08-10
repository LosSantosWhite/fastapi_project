from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, UploadFile, status

from app.modules.products.brands.service import BrandService
from app.modules.products.brands.dependencies import get_brand_service
from app.modules.products.brands.schemas import (
    BrandRetrieve,
    BrandCreate,
    BrandUpdate,
    BrandDelete,
)
from app.modules.products.utils import download_file

from app.modules.products.crud.models import Brand

admin_brand_router = APIRouter(
    prefix="/brand", tags=["CRUD operations for product's brand model"]
)


@admin_brand_router.get(
    "/all", response_model=List[BrandRetrieve], status_code=status.HTTP_200_OK
)
async def get_all_brands_as_staff(
    brand_service: BrandService = Depends(get_brand_service),
):
    return await brand_service.get_all()


@admin_brand_router.get(
    "/{brand_uuid}", response_model=BrandRetrieve, status_code=status.HTTP_200_OK
)
async def get_brand_as_staff(
    brand_uuid: UUID, brand_service: BrandService = Depends(get_brand_service)
):
    return await brand_service.get(id_=brand_uuid)


@admin_brand_router.post(
    "", response_model=BrandRetrieve, status_code=status.HTTP_201_CREATED
)
async def create_brand_as_staff(
    name: str,
    file: UploadFile,
    brand_service: BrandService = Depends(get_brand_service),
):
    schema = BrandCreate(name=name, image_path=file)
    return await brand_service.create(schema=schema)


@admin_brand_router.patch(
    "/{brand_uuid}", response_model=BrandRetrieve, status_code=status.HTTP_200_OK
)
async def update_brand_as_staff(
    brand_uuid: UUID | str,
    name: str = None,
    image_path: UploadFile = None,
    brand_service: BrandService = Depends(get_brand_service),
):
    if not name:
        brand = await brand_service.get(id_=brand_uuid)
        name = brand.name
    if image_path:
        image_path = download_file(name=name, file=image_path, model=Brand)
    schema = BrandUpdate(uuid=brand_uuid, name=name, image_path=image_path)
    return await brand_service.update(schema=schema)


@admin_brand_router.delete("/{brand_uuid}", status_code=status.HTTP_200_OK)
async def delete_brand_as_staff(
    brand_uuid: UUID | str,
    brand_service: BrandService = Depends(get_brand_service),
    permanent: bool = False,
):
    schema = BrandDelete(uuid=brand_uuid)
    return {
        "status": await brand_service.delete(schema=BrandDelete, permanent=permanent),
        "message": "The brand has been deleted!",
    }
