from flask import current_app
from flask import abort
from config import DATABASES
import mysql.connector
import logging


class Database:
    def __init__(self):
        self.db_connection = self.__connect_db()

    def __connect_db(self):
        try:
            db_name = DATABASES['database']
            db_user = DATABASES['user']
            db_password = DATABASES['password']
            db_host = DATABASES['host']
            db_port = DATABASES['port']

            db_connection = mysql.connector.connect(
                database=db_name
                , user=db_user
                , password=db_password
                , host=db_host
                , port=db_port
                , charset='utf8'
            )

            return db_connection

        except mysql.connector.Error as err:
            error_message = '데이터베이스 Error ( {} )'.format(hasattr(err, 'message') and err.message or err)
            logging.error(error_message)
            return abort(500, description="DATABASE_ERROR")

    def execute(self, query, param=None):
        try:
            current_app.logger.info('query : {}'.format(query))
            current_app.logger.info('param : {}'.format(param))
            current_app.logger.info('db connection  : {}'.format(self.db_connection))
            current_app.logger.info('db connection is_connected : {}'.format(self.db_connection.is_connected()))
            current_app.logger.info('db connection ping : {}'.format(self.db_connection.ping(reconnect=True)))
            current_app.logger.info('db connection ping reconnect : {}'.format(self.db_connection.is_connected()))
            if not self.db_connection.is_connected():
                self.db_connection.ping(reconnect=True, attempts=3, delay=0)
                current_app.logger.info('데이터베이스 재접속')
            db_cursor = self.db_connection.cursor(buffered=True, dictionary=True)
            db_cursor.execute(query, param)
            current_app.logger.info('데이터베이스 쿼리 실행')
            return db_cursor

        except mysql.connector.Error as err:
            error_message = '데이터베이스 Error ( {} )'.format(hasattr(err, 'message') and err.message or err)
            logging.error(error_message)
            self.db_connection.rollback()
            return abort(500, description="DATABASE_ERROR")

    def close(self):
        try:
            if self.db_connection is not None:
                self.db_connection.close()
                current_app.logger.info('데이터베이스 접속 종료')

        except mysql.connector.Error as err:
            error_message = '데이터베이스 Error ( {} )'.format(hasattr(err, 'message') and err.message or err)
            logging.error(error_message)
            return abort(500, description="DATABASE_ERROR")

    def rollback(self):
        try:
            if self.db_connection:
                self.db_connection.rollback()
            return True

        except mysql.connector.Error as err:
            error_message = '데이터베이스 Error ( {} )'.format(hasattr(err, 'message') and err.message or err)
            logging.error(error_message)
            return abort(500, description="DATABASE_ERROR")

    def commit(self):
        try:
            if self.db_connection:
                self.db_connection.commit()
            return True

        except mysql.connector.Error as err:
            error_message = '데이터베이스 Error ( {} )'.format(hasattr(err, 'message') and err.message or err)
            logging.error(error_message)
            return abort(500, description="DATABASE_ERROR")

    def start_transaction(self):
        try:
            if self.db_connection:
                self.execute("START TRANSACTION")
                self.execute("SET AUTOCOMMIT=0")
            return True

        except mysql.connector.Error as err:
            error_message = '데이터베이스 Error ( {} )'.format(hasattr(err, 'message') and err.message or err)
            logging.error(error_message)
            return abort(500, description="DATABASE_ERROR")
