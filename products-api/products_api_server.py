import logging
import traceback

import uvicorn
from fastapi import FastAPI, Header
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response
from starlette.status import *

from app import products_service
from app.model.dto.product_dto import ProductCreateDto, ProductPatchDto, ProductUpdateDto
from app.model.product import Product
from app.security import cognito_auth
from exceptions import ApiException, exceptions, exception_response_formatter

api_server = FastAPI()

origins = [
    "*"
]

api_server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

UPDATE_ONLY_FILLED_FIELDS = True
UPDATE_ALL_FIELDS = False

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def __handle_unexpected_exception(response) -> None:
    logger.error(traceback.format_exc())

    response.status_code = HTTP_500_INTERNAL_SERVER_ERROR
    return {}


def __handle_rest_api_exception(response: Response, api_exception: ApiException) -> None:
    logger.info(traceback.format_exc())

    __log_rest_api_exception(api_exception)
    response.status_code = api_exception.http_status.code
    return exception_response_formatter.get_body(api_exception)


def __log_rest_api_exception(api_exception: ApiException) -> None:
    log_message = exception_response_formatter.get_log_message(api_exception)

    if api_exception.type.ERROR == api_exception.type:
        logger.error(log_message)
    else:
        logger.info(log_message)


@api_server.get("/produtos", status_code=HTTP_200_OK)
def get_all_products(response: Response,
                     authorization: str = Header(None)):
    try:
        auth_user = cognito_auth.verify_token(authorization)
        products: [] = products_service.get_products(auth_user.id)
        for product in products:
            del product.user_id
        return products
    except ApiException as exception:
        return __handle_rest_api_exception(response, exception)
    except Exception as exception:
        return __handle_unexpected_exception(response)


@api_server.get("/produtos/{product_id}", status_code=HTTP_200_OK)
def get_product(product_id: str,
                response: Response,
                authorization: str = Header(None)):
    try:
        auth_user = cognito_auth.verify_token(authorization)
        validate_product_id(product_id)
        product: Product = products_service.get_product(auth_user.id, product_id)
        del product.user_id
        return product
    except ApiException as exception:
        return __handle_rest_api_exception(response, exception)
    except Exception as exception:
        return __handle_unexpected_exception(response)


@api_server.post("/produtos", status_code=HTTP_201_CREATED)
def create_product(product_dto: ProductCreateDto,
                   response: Response,
                   authorization: str = Header(None)):
    try:
        auth_user = cognito_auth.verify_token(authorization)
        product_dto.validate_model()
        product: Product = product_dto.parse_to_product()
        product.user_id = auth_user.id

        products_service.create_product(product)

        response.headers.append("Location", "/produtos/{}".format(product.id))
        return {}
    except ApiException as exception:
        return __handle_rest_api_exception(response, exception)
    except Exception as exception:
        return __handle_unexpected_exception(response)


@api_server.put("/produtos/{product_id}", status_code=HTTP_200_OK)
def update_product(product_id: str,
                   product_dto: ProductUpdateDto,
                   response: Response,
                   authorization: str = Header(None)):
    try:
        auth_user = cognito_auth.verify_token(authorization)
        validate_product_id(product_id)
        product_dto.validate_model()

        product: Product = product_dto.parse_to_product()
        product.id = product_id
        product.user_id = auth_user.id

        products_service.update_product(product, UPDATE_ALL_FIELDS)
        return {}
    except ApiException as exception:
        return __handle_rest_api_exception(response, exception)
    except Exception as exception:
        return __handle_unexpected_exception(response)


@api_server.patch("/produtos/{product_id}", status_code=HTTP_200_OK)
def patch_product(product_id: str,
                  product_dto: ProductPatchDto,
                  response: Response,
                  authorization: str = Header(None)):
    try:
        auth_user = cognito_auth.verify_token(authorization)
        validate_product_id(product_id)
        product_dto.validate_model()

        product: Product = product_dto.parse_to_product()
        product.id = product_id
        product.user_id = auth_user.id

        products_service.update_product(product, UPDATE_ONLY_FILLED_FIELDS)
        return {}
    except ApiException as exception:
        return __handle_rest_api_exception(response, exception)
    except Exception as exception:
        return __handle_unexpected_exception(response)


@api_server.delete("/produtos/{product_id}", status_code=HTTP_204_NO_CONTENT)
def delete_product(product_id: str,
                   response: Response,
                   authorization: str = Header(None)):
    try:
        auth_user = cognito_auth.verify_token(authorization)
        validate_product_id(product_id)
        products_service.delete_product(auth_user.id, product_id)
        return {}
    except ApiException as exception:
        return __handle_rest_api_exception(response, exception)
    except Exception as exception:
        return __handle_unexpected_exception(response)


def validate_product_id(product_id: str):
    if product_id is None or len(product_id) != 36:
        exception = exceptions.get(exceptions.FIELD_CONSTRAINT_VIOLATION_EXCEPTION)
        exception.append_validation_error("O id do produto é inválido", "product_id")
        raise exception


if __name__ == "__main__":
    uvicorn.run(api_server, host="0.0.0.0", port=8080)