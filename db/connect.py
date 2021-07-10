from flask import current_app
from config import DATABASES
import mysql.connector
import logging


def init():
    db_name = DATABASES['database']
    db_user = DATABASES['user']
    db_password = DATABASES['password']
    db_host = DATABASES['host']
    db_port = DATABASES['port']

    try:
        db_connection = mysql.connector.connect(
            database=db_name
            , user=db_user
            , password=db_password
            , host=db_host
            , port=db_port
            , charset='utf8'
        )

        return db_connection

    except Exception as e:
        error_message = '데이터베이스 접속 실패 ( {} )'.format(hasattr(e, 'message') and e.message or e)
        logging.error(error_message)


def execute(db_connection, query, param=None):
    current_app.logger.info('query : {}'.format(query))
    current_app.logger.info('param : {}'.format(param))
    current_app.logger.info('db connection  : {}'.format(db_connection))
    current_app.logger.info('db connection is_connected : {}'.format(db_connection.is_connected()))
    current_app.logger.info('db connection ping : {}'.format(db_connection.ping(reconnect=True)))
    current_app.logger.info('db connection ping reconnect : {}'.format(db_connection.is_connected()))
    if not db_connection.is_connected():
        db_connection.ping(reconnect=True, attempts=3, delay=0)
        current_app.logger.info('데이터베이스 재접속')
    db_cursor = db_connection.cursor(buffered=True, dictionary=True)
    db_cursor.execute(query, param)
    current_app.logger.info('데이터베이스 쿼리 실행')
    return db_cursor


def close(db_cursor):
    try:
        if db_cursor is not None:
            db_cursor.close()
            current_app.logger.info('데이터베이스 접속 종료')

    except Exception as e:
        error_message = '데이터베이스 접속 종료 실패 ( {} )'.format(hasattr(e, 'message') and e.message or e)
        logging.error(error_message)


def rollback(db_cursor):
    try:
        if db_cursor:
            db_cursor.rollback()
        return True

    except Exception as e:
        error_message = '데이터베이스 rollback 실패 ( {} )'.format(hasattr(e, 'message') and e.message or e)
        logging.error(error_message)


def commit(db_cursor):
    try:
        if db_cursor:
            db_cursor.commit()
        return True

    except Exception as e:
        error_message = '데이터베이스 rollback 실패 ( {} )'.format(hasattr(e, 'message') and e.message or e)
        logging.error(error_message)


def start_transaction(db_cursor):
    try:
        if db_cursor:
            execute(db_cursor, "START TRANSACTION")
            execute(db_cursor, "SET AUTOCOMMIT=0")
        return True

    except Exception as e:
        error_message = '데이터베이스 start_transaction 실패 ( {} )'.format(hasattr(e, 'message') and e.message or e)
        logging.error(error_message)