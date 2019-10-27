import logging
import json
import os

import pymysql as pymysql
from app.aws import secret_manager

environment = os.getenv("APP_ENVIRONMENT", "dev")

db_host = os.getenv("DB_HOST", "localhost")
db_port = int(os.getenv("DB_PORT", 3306))
db_user = os.getenv("DB_USER", "root")
db_pass = os.getenv("DB_PASS", "devPassword")
db_name = os.getenv("DB_SCHEMA", "python-products-api")
db_conn_timeout = int(os.getenv("DB_TIMEOUT", 30))

aws_secret_name = os.getenv("AWS_SECRET_NAME", "python-products-api")
aws_secret_service = os.getenv("AWS_SECRET_SERVICE", "secretsmanager")
aws_region = os.getenv("AWS_REGION", "us-east-1")
aws_secret_key = os.getenv("AWS_SECRET_KEY", "secret")


def get_db_config() -> dict:
    logging.info("db_host: {}".format(db_host))
    logging.info("db_port: {}".format(db_port))
    logging.debug("db_user: {}".format(db_user))
    logging.debug("db_pass: {}".format(db_pass))
    logging.info("db_name: {}".format(db_name))
    logging.info("db_conn_timeout: {}".format(db_conn_timeout))
    logging.info("aws_secret_name: {}".format(aws_secret_name))
    logging.info("aws_secret_service: {}".format(aws_secret_service))
    logging.info("aws_region: {}".format(aws_region))
    logging.info("aws_secret_key: {}".format(aws_secret_key))

    username = db_user
    password = db_pass

    if not environment == "dev":
        logging.info("Connecting to secret manager")
        secret = json.loads(secret_manager.get_secret())
        username = secret.get('username')
        password = secret.get('password')

    return {'host': db_host,
     'port': db_port,
     'db': db_name,
     'user': username,
     'passwd': password,
     'charset': 'utf8mb4',
     'cursorclass': pymysql.cursors.DictCursor,
     'connect_timeout': db_conn_timeout}
