from fastapi import APIRouter

from app.config import config

from app.modules.products.api.v1 import admin_products_router

admin_router = APIRouter(prefix=f"{config.prefixes.admin}/v1")

admins_routers = (admin_products_router,)

for router in admins_routers:
    admin_router.include_router(router)
