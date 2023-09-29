from typing import List

from fastapi import Depends, APIRouter

from app.modules.products.categories.service import CategoryService
from app.modules.products.categories.dependencies import get_category_service
from app.modules.products.categories.schemas import CategoryRetrieve

admin_category_router = APIRouter(
    prefix="/category", tags=["CRUD operations for product's category model"]
)


@admin_category_router.get("/all", response_model=List[CategoryRetrieve])
async def get_all_as_staff(
    category_service: CategoryService = Depends(get_category_service),
):
    return await category_service.get_all()


@admin_category_router.get("/{category_id}", response_model=CategoryRetrieve)
async def get(
    category_id: int,
    category_service: CategoryService = Depends(get_category_service),
):
    return await category_service.get(id_=category_id)
