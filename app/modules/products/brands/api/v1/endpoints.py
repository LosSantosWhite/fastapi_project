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

admin_brand_router = APIRouter(
    prefix="/brand", tags=["CRUD operations for product's brand model"]
)


@admin_brand_router.get(
    "/all", status_code=status.HTTP_200_OK, response_model=List[BrandRetrieve]
)
async def get_all_brands_as_staff(
    brand_service: BrandService = Depends(get_brand_service),
):
    result = await brand_service.get_all()
    return result


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
    return await brand_service.create(data=dict(name=name), file=file)


@admin_brand_router.patch(
    "/{brand_uuid}", response_model=BrandRetrieve, status_code=status.HTTP_200_OK
)
async def update_brand_as_staff(
    brand_uuid: UUID | str,
    name: str = None,
    file: UploadFile = None,
    brand_service: BrandService = Depends(get_brand_service),
):
    return await brand_service.update(
        schema=BrandUpdate(uuid=brand_uuid, name=name), file=file
    )


@admin_brand_router.delete("/{brand_uuid}", status_code=status.HTTP_200_OK)
async def delete_brand_as_staff(
    brand_uuid: UUID | str,
    brand_service: BrandService = Depends(get_brand_service),
):
    return {
        "status": await brand_service.delete(schema=BrandDelete(uuid=brand_uuid)),
        "message": "The brand has been deleted!",
    }
