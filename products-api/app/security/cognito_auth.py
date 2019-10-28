import cognitojwt
from cognitojwt import CognitoJWTException
from exceptions import exceptions
import traceback
import logging

from app import environment_config


def verify_token(id_token: str):
    logging.info("Verifying token: {}".format(id_token))
    if id_token is None or not id_token.startswith("Bearer "):
        exception = exceptions.get(exceptions.USER_NOT_AUTHORIZED_EXCEPTION)
        exception.append_to_log("id_token: {}".format(id_token))
        exception.append_to_log("cause: Bearer not present")
        raise exception

    token = id_token.replace("Bearer ", "")

    try:
        verified_claims: dict = cognitojwt.decode(
            token,
            environment_config.aws_cognito_region,
            environment_config.aws_cognito_user_pool_id,
            testmode=not environment_config.aws_cognito_enabled
        )
    except CognitoJWTException as jwt_exception:
        exception = exceptions.get(exceptions.USER_NOT_AUTHORIZED_EXCEPTION)
        exception.append_to_log("id_token: {}".format(id_token))
        exception.append_to_log("exception: {}".format(traceback.format_exc()))
        raise exception
    except ValueError as value_exception:
        exception = exceptions.get(exceptions.USER_NOT_AUTHORIZED_EXCEPTION)
        exception.append_to_log("id_token: {}".format(id_token))
        exception.append_to_log("exception: {}".format(traceback.format_exc()))
        raise exception

    logging.info("Token validated successfully")
