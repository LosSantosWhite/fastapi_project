from fastapi import APIRouter

from app.config import config
from app.modules.products.colors.api.v1.endpoints import admin_colors_router

from app.modules.products.brands.api.v1.endpoints import admin_brand_router

admin_router = APIRouter(prefix=f"{config.prefixes.admin}/v1")

admins_routers = (admin_colors_router, admin_brand_router)

for router in admins_routers:
    admin_router.include_router(router)
