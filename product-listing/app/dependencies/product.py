from app.services.product_service import ProductService
from app.services.product_service_impl import ProductServiceImpl

class ProductDep:
    def __init__(self):
        self.product_service: ProductService = ProductServiceImpl()