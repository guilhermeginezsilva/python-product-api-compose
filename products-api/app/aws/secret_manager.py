import boto3
import base64
from botocore.exceptions import ClientError
import logging
from app import environment_config


def get_secret():
    session = boto3.session.Session()
    client = session.client(
        service_name=environment_config.aws_secret_service,
        region_name=environment_config.aws_region
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=environment_config.aws_secret_name)
    except ClientError as error:
        logging.error('Error on get secret keys: {}'.format(error))
        return '{}'

    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return secret
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return decoded_binary_secret
