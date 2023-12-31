from fastapi import APIRouter

from app.modules.products.colors.api.v1.endpoints import admin_colors_router
from app.modules.products.brands.api.v1.endpoints import admin_brand_router
from app.modules.products.collections.api.v1.endpoints import admin_collection_router
from app.modules.products.categories.api.v1.endpoints import admin_category_router

admin_products_router = APIRouter(prefix="/products", tags=["Admin products"])


# admin_collection_router.include_router(admin_model_router)
admin_brand_router.include_router(admin_collection_router)


admin_routers = (
    admin_colors_router,
    admin_brand_router,
    admin_category_router,
)

for router in admin_routers:
    admin_products_router.include_router(router)
