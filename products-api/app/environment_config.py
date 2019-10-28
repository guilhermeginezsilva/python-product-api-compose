import logging
import os

import pymysql as pymysql

environment = os.getenv("APP_ENVIRONMENT", "dev")

db_host = os.getenv("DB_HOST", "localhost")
db_port = int(os.getenv("DB_PORT", 3306))
db_user = os.getenv("DB_USER", "root")
db_pass = os.getenv("DB_PASS", "devPassword")
db_name = os.getenv("DB_SCHEMA", "python-products-api")
db_conn_timeout = int(os.getenv("DB_TIMEOUT", 30))

aws_cognito_region = os.getenv("AWS_COGNITO_REGION", None)
aws_cognito_user_pool_id = os.getenv("AWS_COGNITO_USER_POOL_ID", None)
aws_cognito_enabled = bool(os.getenv("AWS_COGNITO_ENABLED", True))

logging.info("db_host: {}".format(db_host))
logging.info("db_port: {}".format(db_port))
logging.debug("db_user: {}".format(db_user))
logging.debug("db_pass: {}".format(db_pass))
logging.info("db_name: {}".format(db_name))
logging.info("db_conn_timeout: {}".format(db_conn_timeout))


def get_db_config() -> dict:

    return {'host': db_host,
            'port': db_port,
            'db': db_name,
            'user': db_user,
            'passwd': db_pass,
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor,
            'connect_timeout': db_conn_timeout
            }
