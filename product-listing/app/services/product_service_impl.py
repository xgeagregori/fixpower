from app.schemas.product import (
    ComponentCreate,
    DamagedProductCreate,
    RefurbishedProductCreate,
    ProductCategory,
    ProductCreate,
    ProductOut,
)
from app.services.product_service import ProductService, ProductFactory


class ProductServiceImpl(ProductService):
    def create_product(self, product_create: ProductCreate):
        category = product_create.category

        if category == ProductCategory.COMPONENT:
            product = ComponentFactory().create_product(product_create)
        elif category == ProductCategory.DAMAGED_PRODUCT:
            product = DamagedProductFactory().create_product(product_create)
        elif category == ProductCategory.REFURBISHED_PRODUCT:
            product = RefurbishedFactory().create_product(product_create)

        return product


class ComponentFactory(ProductFactory):
    def create_product(self, product_create: ProductCreate):
        return ComponentCreate(**product_create.dict())


class DamagedProductFactory(ProductFactory):
    def create_product(self, product_create: ProductCreate):
        return DamagedProductCreate(**product_create.dict())


class RefurbishedFactory(ProductFactory):
    def create_product(self, product_create: ProductCreate):
        print(product_create.dict())
        return RefurbishedProductCreate(**product_create.dict())
