import uuid

from app.database import products_dao
from app.model.product import Product


def get_products(auth_id: str) -> []:
    return products_dao.find_all(auth_id)


def get_product(auth_id: str, product_id: str) -> Product:
    return products_dao.find_one(auth_id, product_id)


def create_product(product: Product) -> None:
    product.id = str(uuid.uuid4())
    products_dao.insert(product)


def update_product(product: Product, only_filled_fields: bool) -> None:
    db_product: Product = products_dao.find_one(product.user_id, product.id)

    if only_filled_fields:
        __copy_product_ignoring_null(product, db_product)
    else:
        db_product = product

    products_dao.update(db_product)


def __copy_product_ignoring_null(origin_product: Product, destiny_product: Product) -> None:
    if origin_product.name is not None:
        destiny_product.name = origin_product.name
    if origin_product.categories is not None:
        destiny_product.categories = origin_product.categories
    if origin_product.price is not None:
        destiny_product.price = origin_product.price
    if origin_product.url is not None:
        destiny_product.url = origin_product.url


def delete_product(auth_id: str, product_id: str) -> None:
    if product_id is None:
        return

    products_dao.delete(auth_id, product_id)