import copy
from exceptions.api_exception import ApiException
from exceptions.http_status import HttpStatus
from exceptions.exception_type import ExceptionType

__SERVER_ERROR_LOGGING_MESSAGE = "An unexpected exception has been thrown"
__SERVER_ERROR_RESPONSE_MESSAGE = "Houve um erro inesperado na API por favor tente novamente daqui alguns instantes. " +\
                                  "Caso o erro persista por favor entre em contato com o nosso time de suporte"
__SERVER_ERROR_EXCEPTION_CODE = 9000

DEFAULT_SERVER_ERROR_MESSAGE = "DEFAULT_SERVER_ERROR_MESSAGE"
FIELD_CONSTRAINT_VIOLATION_EXCEPTION = "FIELD_CONSTRAINT_VIOLATION_EXCEPTION"

USER_NOT_AUTHORIZED_EXCEPTION = "USER_NOT_AUTHORIZED_EXCEPTION"

FIELD_VALUE_CONSTRAINT_VIOLATION_EXCEPTION = "FIELD_CONSTRAINT_VIOLATION_EXCEPTION"
UNAVAILABLE_CATEGORY_EXCEPTION = "UNAVAILABLE_CATEGORY_EXCEPTION"
PRODUCT_NOT_FOUND_EXCEPTION = "PRODUCT_NOT_FOUND_EXCEPTION"

PRODUCT_SAVE_TO_DATABASE_EXCEPTION = "PRODUCT_SAVE_TO_DATABASE_EXCEPTION"
CATEGORY_SAVE_TO_DATABASE_EXCEPTION = "CATEGORY_SAVE_TO_DATABASE_EXCEPTION"

__EXCEPTION_NOT_FOUND:ApiException = ApiException(
        "EXCEPTION_NOT_FOUND",
        __SERVER_ERROR_EXCEPTION_CODE,
        __SERVER_ERROR_LOGGING_MESSAGE,
        __SERVER_ERROR_RESPONSE_MESSAGE,
        HttpStatus.INTERNAL_SERVER_ERROR,
        ExceptionType.ERROR)


__exceptions_map = {
    DEFAULT_SERVER_ERROR_MESSAGE: ApiException(
        DEFAULT_SERVER_ERROR_MESSAGE,
        __SERVER_ERROR_EXCEPTION_CODE,
        __SERVER_ERROR_LOGGING_MESSAGE,
        __SERVER_ERROR_RESPONSE_MESSAGE,
        HttpStatus.INTERNAL_SERVER_ERROR,
        ExceptionType.ERROR),

    FIELD_CONSTRAINT_VIOLATION_EXCEPTION: ApiException(
        FIELD_CONSTRAINT_VIOLATION_EXCEPTION,
        "8000",
        "Field constraint violation",
        "Encontramos problemas ao validar os campos de entrada",
        HttpStatus.BAD_REQUEST,
        ExceptionType.VALIDATION),

    FIELD_VALUE_CONSTRAINT_VIOLATION_EXCEPTION: ApiException(
        FIELD_VALUE_CONSTRAINT_VIOLATION_EXCEPTION,
        "8001",
        "Field value constraint violation",
        "Encontramos problemas ao validar os campos de entrada",
        HttpStatus.UNPROCESSABLE_ENTITY,
        ExceptionType.VALIDATION),

    USER_NOT_AUTHORIZED_EXCEPTION: ApiException(
        USER_NOT_AUTHORIZED_EXCEPTION,
        "7000",
        "The user authentication failed",
        "Usuário não autorizado, favor verifique suas credenciais",
        HttpStatus.NO_CONTENT,
        ExceptionType.BUSINESS_RULES),

    UNAVAILABLE_CATEGORY_EXCEPTION: ApiException(
        UNAVAILABLE_CATEGORY_EXCEPTION,
        "0001",
        "Category not available",
        "A categoria enviada não existe, favor enviar apenas categorias existentes",
        HttpStatus.CONFLICT,
        ExceptionType.BUSINESS_RULES),

    PRODUCT_NOT_FOUND_EXCEPTION: ApiException(
        PRODUCT_NOT_FOUND_EXCEPTION,
        "0002",
        "Product not found",
        "O produto solicitado não foi encontrado",
        HttpStatus.NO_CONTENT,
        ExceptionType.BUSINESS_RULES),

    PRODUCT_SAVE_TO_DATABASE_EXCEPTION: ApiException(
        PRODUCT_SAVE_TO_DATABASE_EXCEPTION,
        __SERVER_ERROR_EXCEPTION_CODE,
        "Couldn't save the product on the database",
        __SERVER_ERROR_RESPONSE_MESSAGE,
        HttpStatus.INTERNAL_SERVER_ERROR,
        ExceptionType.ERROR),

    CATEGORY_SAVE_TO_DATABASE_EXCEPTION: ApiException(
        CATEGORY_SAVE_TO_DATABASE_EXCEPTION,
        __SERVER_ERROR_EXCEPTION_CODE,
        "Couldn't save the category on the database",
        __SERVER_ERROR_RESPONSE_MESSAGE,
        HttpStatus.INTERNAL_SERVER_ERROR,
        ExceptionType.ERROR)
}


def get(exception_name: str) -> ApiException:
    found_exception = __exceptions_map.get(exception_name, __EXCEPTION_NOT_FOUND)

    return copy.deepcopy(found_exception)

