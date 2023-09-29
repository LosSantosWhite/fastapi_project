from app.modules.products.base.service import ProductServiceBase


class CollectionService(ProductServiceBase):
    duplicate_message = "Collection already exists"
