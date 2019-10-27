from app.model.product import Product
import uuid
from app.database import products_dao


def get_products() -> []:
    return products_dao.find_all()


def get_product(product_id: str) -> Product:
    return products_dao.find_one(product_id)


def create_product(product: Product) -> None:
    product.id = str(uuid.uuid4())
    products_dao.insert(product)


def update_product(product: Product, only_filled_fields: bool) -> None:
    db_product: Product = products_dao.find_one(product.id)

    if only_filled_fields:
        __copy_product_ignoring_null(product, db_product)
    else:
        db_product = product

    products_dao.update(db_product)


def __copy_product_ignoring_null(origin_product: Product, destiny_product: Product) -> None:
    if origin_product.name:
        destiny_product.name = origin_product.name
    if origin_product.categories:
        destiny_product.categories = origin_product.categories
    if origin_product.price:
        destiny_product.price = origin_product.price
    if origin_product.url:
        destiny_product.url = origin_product.url


def delete_product(product_id: str) -> None:
    if product_id is None:
        return

    products_dao.delete(product_id)