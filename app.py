import os
import logging
from datetime import datetime
from flask import Flask
from config import DATABASES
from logging.handlers import RotatingFileHandler
from admin.admin_service import AdminService
from admin.admin_view import AdminView

def get_db_config():
    dbconfig = {
        'database': DATABASES['database'],
        'user': DATABASES['user'],
        'password': DATABASES['password'],
        'host': DATABASES['host'],
        'port': DATABASES['port'],
    }

    return dbconfig

class Services:
    pass

def create_app():
    app = Flask(__name__)

    # Service Layer
    services = Services
    services.admin_service = AdminService()

    # endpoint
    AdminView.create_endpoint(app, services)

    # logging
    if not os.path.exists('log'):
        os.mkdir('log')

    today_data = datetime.now().strftime('%Y-%m-%d')
    formatter = logging.Formatter("[%(asctime)s] [%(process)d] %(levelname)s - %(message)s")
    handler = RotatingFileHandler('log/square-admin' + str(today_data) + '.log'
                                  , maxBytes=10000000, backupCount=5
                                  , encoding='utf-8')
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(level=logging.INFO)

    return app


