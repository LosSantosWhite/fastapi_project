from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, UploadFile, status, Request

from app.modules.products.brands.service import BrandService
from app.modules.products.brands.dependencies import get_brand_service
from app.modules.products.base.schemas import (
    ProductRetrieve,
    ProductCreate,
    ProductUpdate,
    ProductDelete,
)
from app.modules.products.utils import download_file

from app.modules.products.crud.models import Brand

admin_brand_router = APIRouter(
    prefix="/brand", tags=["CRUD operations for product's brand model"]
)


@admin_brand_router.get(
    "/all", status_code=status.HTTP_200_OK, response_model=List[ProductRetrieve]
)
async def get_all_brands_as_staff(
    brand_service: BrandService = Depends(get_brand_service),
):
    return await brand_service.get_all()


@admin_brand_router.get(
    "/{brand_uuid}", response_model=ProductRetrieve, status_code=status.HTTP_200_OK
)
async def get_brand_as_staff(
    brand_uuid: UUID, brand_service: BrandService = Depends(get_brand_service)
):
    return await brand_service.get(id_=brand_uuid)


@admin_brand_router.post(
    "", response_model=ProductRetrieve, status_code=status.HTTP_201_CREATED
)
async def create_brand_as_staff(
    name: str,
    file: UploadFile,
    brand_service: BrandService = Depends(get_brand_service),
):
    schema = ProductCreate(name=name)
    return await brand_service.create(schema=schema, file=file)


@admin_brand_router.patch(
    "/{brand_uuid}", response_model=ProductRetrieve, status_code=status.HTTP_200_OK
)
async def update_brand_as_staff(
    brand_uuid: UUID | str,
    name: str = None,
    file: UploadFile = None,
    brand_service: BrandService = Depends(get_brand_service),
):
    return await brand_service.update(
        schema=ProductUpdate(uuid=brand_uuid, name=name), file=file
    )


@admin_brand_router.delete("/{brand_uuid}", status_code=status.HTTP_200_OK)
async def delete_brand_as_staff(
    brand_uuid: UUID | str,
    brand_service: BrandService = Depends(get_brand_service),
    permanent: bool = False,
):
    schema = ProductDelete(uuid=brand_uuid)
    return {
        "status": await brand_service.delete(schema=ProductDelete, permanent=permanent),
        "message": "The brand has been deleted!",
    }
