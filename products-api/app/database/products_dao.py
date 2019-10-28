import logging

import pymysql
from pymysql import OperationalError

from app import environment_config
from app.model.product import Product
from exceptions import exceptions, ApiException

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

SQL_QUERY_SELECT_ALL_PRODUCTS = "SELECT ID, NAME, PRICE, URL FROM TB_PRODUCT WHERE USER_ID = %s"
SQL_QUERY_SELECT_PRODUCT = "SELECT ID, NAME, PRICE, URL FROM TB_PRODUCT WHERE ID = %s AND USER_ID = %s"
SQL_QUERY_INSERT_PRODUCT = "INSERT INTO TB_PRODUCT (ID, NAME, PRICE, URL, USER_ID) VALUES (%s, %s, %s, %s, %s)"
SQL_QUERY_UPDATE_PRODUCT = "UPDATE TB_PRODUCT SET NAME=%s, PRICE=%s, URL=%s WHERE ID = %s AND USER_ID = %s"
SQL_QUERY_DELETE_PRODUCT = "DELETE FROM TB_PRODUCT WHERE ID = %s AND USER_ID = %s"

SQL_QUERY_SELECT_ALL_CATEGORIES_BY_PRODUCT = "SELECT NAME, PRODUCT_ID FROM TB_CATEGORY WHERE PRODUCT_ID = %s"
SQL_QUERY_INSERT_CATEGORY = "INSERT INTO TB_CATEGORY (NAME, PRODUCT_ID) VALUES (%s, %s)"
SQL_QUERY_DELETE_CATEGORY_BY_PRODUCT = "DELETE FROM TB_CATEGORY WHERE PRODUCT_ID = %s"


def find_all(auth_id: str) -> []:
    conn = None
    try:
        conn = pymysql.connect(**environment_config.get_db_config())
        products = []

        with conn:
            cursor = conn.cursor()
            cursor.execute(SQL_QUERY_SELECT_ALL_PRODUCTS, auth_id)

            product_rows = cursor.fetchall()
            for product_row in product_rows:
                product = Product(
                    product_row["NAME"],
                    [],
                    product_row["PRICE"],
                    product_row["URL"],
                    product_row["ID"]
                )

                cursor.execute(SQL_QUERY_SELECT_ALL_CATEGORIES_BY_PRODUCT, product.id)
                category_rows = cursor.fetchall()

                for category_row in category_rows:
                    product.categories.append(str(category_row["NAME"]))

                products.append(product)

        return products

    except OperationalError as error:
        logger.error("ERROR: Unexpected error: Could not connect to MySql instance: {}".format(error))
        if conn:
            conn.rollback()
        raise error
    except ApiException as error:
        if conn:
            conn.rollback()
        raise error
    except Exception as error:
        logger.error("ERROR: Unexpected error: {}".format(error))
        if conn:
            conn.rollback()
        raise error
    finally:
        if conn:
            conn.close()


def find_one(auth_id: str, product_id: str) -> Product:
    conn = None
    try:
        conn = pymysql.connect(**environment_config.get_db_config())

        with conn:
            cursor = conn.cursor()
            cursor.execute(SQL_QUERY_SELECT_PRODUCT, (product_id, auth_id))

            result = cursor.fetchone()

            if cursor.rowcount == 0:
                exception = exceptions.get(exceptions.PRODUCT_NOT_FOUND_EXCEPTION)
                exception.append_to_log("Couldn't find product: {}".format(product_id))
                raise exception

            product = Product(
                result["NAME"],
                [],
                result["PRICE"],
                result["URL"],
                result["ID"]
            )

            cursor.execute(SQL_QUERY_SELECT_ALL_CATEGORIES_BY_PRODUCT, product_id)
            rows = cursor.fetchall()

            for row in rows:
                product.categories.append(str(row["NAME"]))

            return product

    except OperationalError as error:
        logger.error("ERROR: Unexpected error: Could not connect to MySql instance: {}".format(error))
        if conn:
            conn.rollback()
        raise error
    except ApiException as error:
        if conn:
            conn.rollback()
        raise error
    except Exception as error:
        logger.error("ERROR: Unexpected error: {}".format(error))
        if conn:
            conn.rollback()
        raise error
    finally:
        if conn:
            conn.close()


def insert(product: Product):

    conn = None
    try:
        conn = pymysql.connect(**environment_config.get_db_config())
        conn.begin()

        with conn:
            cursor = conn.cursor()
            cursor.execute(SQL_QUERY_INSERT_PRODUCT,
                           (product.id, product.name, product.price, product.url, product.user_id))

            if cursor.rowcount == 0:
                exception = exceptions.get(exceptions.PRODUCT_SAVE_TO_DATABASE_EXCEPTION)
                exception.append_to_log("Event: Create")
                exception.append_to_log("Product: {}".format(str(product)))
                raise exception

            for category in product.categories:
                cursor.execute(SQL_QUERY_INSERT_CATEGORY, (category, product.id))

                if cursor.rowcount != 1:
                    exception = exceptions.get(exceptions.CATEGORY_SAVE_TO_DATABASE_EXCEPTION)
                    exception.append_to_log("Event: Create")
                    exception.append_to_log("Product: {}".format(str(product)))
                    exception.append_to_log("Category: {}".format(str(category)))
                    raise exception

            conn.commit()

    except OperationalError as error:
        logger.error("ERROR: Unexpected error: Could not connect to MySql instance: {}".format(error))
        if conn:
            conn.rollback()
        raise error
    except ApiException as error:
        if conn:
            conn.rollback()
        raise error
    except Exception as error:
        logger.error("ERROR: Unexpected error: {}".format(error))
        if conn:
            conn.rollback()
        raise error
    finally:
        if conn:
            conn.close()


def update(product: Product):

    conn = None
    try:
        conn = pymysql.connect(**environment_config.get_db_config())
        conn.begin()

        with conn:
            cursor = conn.cursor()
            cursor.execute(SQL_QUERY_UPDATE_PRODUCT, (product.name, product.price, product.url, product.id, product.user_id))

            cursor.execute(SQL_QUERY_DELETE_CATEGORY_BY_PRODUCT, product.id)
            for category in product.categories:
                cursor.execute(SQL_QUERY_INSERT_CATEGORY, (category, product.id))

                if cursor.rowcount != 1:
                    exception = exceptions.get(exceptions.CATEGORY_SAVE_TO_DATABASE_EXCEPTION)
                    exception.append_to_log("Event: Update")
                    exception.append_to_log("Product: {}".format(str(product)))
                    exception.append_to_log("Category: {}".format(str(category)))
                    raise exception

            conn.commit()

    except OperationalError as error:
        logger.error("ERROR: Unexpected error: Could not connect to MySql instance: {}".format(error))
        if conn:
            conn.rollback()
        raise error
    except ApiException as error:
        if conn:
            conn.rollback()
        raise error
    except Exception as error:
        logger.error("ERROR: Unexpected error: {}".format(error))
        if conn:
            conn.rollback()
        raise error
    finally:
        if conn:
            conn.close()


def delete(auth_id: str, product_id: str):
    conn = None
    try:

        conn = pymysql.connect(**environment_config.get_db_config())
        conn.begin()

        with conn:
            cursor = conn.cursor()

            cursor.execute(SQL_QUERY_SELECT_PRODUCT, (product_id, auth_id))
            cursor.fetchone()
            if cursor.rowcount == 0:
                exception = exceptions.get(exceptions.PRODUCT_NOT_FOUND_EXCEPTION)
                exception.append_to_log("Couldn't find product: {}".format(product_id))
                raise exception

            cursor.execute(SQL_QUERY_DELETE_CATEGORY_BY_PRODUCT, product_id)
            cursor.execute(SQL_QUERY_DELETE_PRODUCT, (product_id, auth_id))
            conn.commit()

    except OperationalError as error:
        logger.error("ERROR: Unexpected error: Could not connect to MySql instance: {}".format(error))
        if conn:
            conn.rollback()
        raise error
    except ApiException as error:
        if conn:
            conn.rollback()
        raise error
    except Exception as error:
        logger.error("ERROR: Unexpected error: {}".format(error))
        if conn:
            conn.rollback()
        raise error
    finally:
        if conn:
            conn.close()
