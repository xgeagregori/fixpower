from fastapi import HTTPException, status

from app.models.product import Component, RefurbishedProduct, DamageProduct, Product
from app.schemas.product import ComponentCreate, DamageProductCreate, RefurbishedProductCreate, ProductCategory, ProductCreate
from app.services.product_service import ProductService, ProductFactory
from app.services.product_listing_service_impl import ProductListingServiceImpl

from uuid import uuid4


class ProductServiceImpl(ProductService):
    def __init__(self):
        self.product_listing_service = ProductListingServiceImpl()

    def create_Product(self, product_listing_id, product_category: ProductCategory, product_create: ProductCreate):
        product: Product = None
        if product_category == ProductCategory.component:
            factory = ComponantFactory()
            product = factory.create_Product(product_create)
        elif product_category == ProductCategory.damage_product:
            factory = DamageProductFactory()
            product = factory.create_Product(product_create)
        elif product_category == ProductCategory.refurbishedproduct:
            factory = RefurbishedFactory()
            product = factory.create_Product(product_create)

        product_listing = self.product_listing_service.get_product_listing_by_id(
            product_listing_id
        )
        product_listing.product = product
        return product


class ComponantFactory(ProductFactory):
    def create_Product(self, product: ComponentCreate):
        generated_id = str(uuid4())
        return Component(id=generated_id, **product.dict())


class DamageProductFactory(ProductFactory):
    def create_Product(self, product: DamageProductCreate):
        generated_id = str(uuid4())
        return RefurbishedProduct(id=generated_id, **product.dict())


class RefurbishedFactory(ProductFactory):
    def create_Product(self, product: RefurbishedProductCreate):
        generated_id = str(uuid4())
        return DamageProduct(id=generated_id, **product.dict())
