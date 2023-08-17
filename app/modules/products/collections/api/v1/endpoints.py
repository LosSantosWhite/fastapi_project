from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, UploadFile, status

from app.modules.products.collections.schemas import (
    CollectionCreate,
    CollectionDelete,
    CollectionRetrieve,
    CollectionUpdate,
)
from app.modules.products.collections.dependencies import get_collection_service
from app.modules.products.collections.service import CollectionService

admin_collection_router = APIRouter(
    prefix="/collection", tags=["CRUD operations for product's collection model"]
)


@admin_collection_router.get(
    "/all", response_model=List[CollectionRetrieve], status_code=status.HTTP_200_OK
)
async def get_all_collections_as_staff(
    collection_service: CollectionService = Depends(get_collection_service),
):
    return await collection_service.get_all()


@admin_collection_router.get(
    "/{collection_uuid}",
    response_model=CollectionRetrieve,
    status_code=status.HTTP_200_OK,
)
async def get_collection_as_staff(
    collection_uuid: UUID | str,
    collection_service: CollectionService = Depends(get_collection_service),
):
    return await collection_service.get(id_=collection_uuid)


@admin_collection_router.post(
    "", response_model=CollectionRetrieve, status_code=status.HTTP_201_CREATED
)
async def create_collection_as_staff(
    name: str,
    brand_uuid: UUID | str,
    file: UploadFile,
    collection_service: CollectionService = Depends(get_collection_service),
):
    return await collection_service.create(
        schema=CollectionCreate(name=name, brand_id=brand_uuid), file=file
    )


@admin_collection_router.delete("/{collection_uuid}")
async def delete_collection_as_staff(
    collection_uuid: UUID | str,
    collection_service: CollectionService = Depends(get_collection_service),
):
    return {
        "status": await collection_service.delete(
            schema=CollectionDelete(uuid=collection_uuid)
        ),
        "message": "The collection has been deleted!",
    }


@admin_collection_router.patch(
    "/{collection_uuid}",
    response_model=CollectionRetrieve,
    status_code=status.HTTP_200_OK,
)
async def update_collection_as_staff(  # TODO: переделать все PATCH методы????
    collection_uuid: UUID | str,
    collection_name: str = None,
    brand_id: UUID | str = None,
    file: UploadFile = None,
    collection_service: CollectionService = Depends(get_collection_service),
):
    schema = CollectionUpdate(
        uuid=collection_uuid, name=collection_name, brand_id=brand_id
    )
    return await collection_service.update(schema=schema, file=file)
