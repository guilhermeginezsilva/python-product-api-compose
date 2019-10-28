from exceptions.api_exception import ApiException
from exceptions.exception_handler_json_body import ExceptionHandlerJsonBody


def get_log_message(api_exception: ApiException) -> str:
    message = "\n--- AN EXCEPTION HAS OCCURRED ---\n"
    message += "HTPP STATUS: " + api_exception.http_status.name + "[" + str(api_exception.http_status.code) + "]"
    message += "\nNAME: " + api_exception.name
    message += "\nCODE: " + str(api_exception.code)
    message += "\nPUBLIC MESSAGE: " + api_exception.public_message
    message += "\nLOGGING MESSAGE: " + api_exception.logging_message
    message += "\nVALIDATION MESSAGES: { "
    message += ", ".join(api_exception.validation_errors)
    message += "\n },"
    message += "\nPUBLIC EXTRA DATA: { "
    message += ", ".join(api_exception.external_messages)
    message += "\n },"
    message += "\nLOGGING EXTRA DATA: { "
    message += ", ".join(api_exception.logging_messages)
    message += "\n }"

    return message


def get_body(api_exception: ApiException) -> dict:
    exception_json_body = ExceptionHandlerJsonBody(api_exception.http_status,
                             api_exception.public_message,
                             api_exception.code,
                             api_exception.validation_errors,
                             api_exception.external_messages) \
        .get_json_format_dict()

    if exception_json_body.get("status") is None:
        del exception_json_body["status"]

    if exception_json_body.get("error") is None:
        del exception_json_body["error"]

    if exception_json_body.get("errorCode") is None:
        del exception_json_body["errorCode"]

    if exception_json_body.get("validationErrors") is None or len(exception_json_body.get("validationErrors")) == 0:
        del exception_json_body["validationErrors"]

    if exception_json_body.get("messages") is None or len(exception_json_body.get("messages")) == 0:
        del exception_json_body["messages"]

    return exception_json_body
