import logging
import traceback
from flask import abort
from db.database import Database

class AdminService:
    def __init__(self):
        self.admin_dao = AdminDao()
        self.database = Database()

    def admin_signup(self, data):
        pass

    return admin_signup_view_data

except Exception as err:
    error_message = 'Exception execute Error ( {} )'.format(hasattr(err, 'message') and err.message or err)
    logging.error(error_message)
    error_info = 'Exception Error info ( {} )'.format(traceback.format_exc())
    logging.error(error_info)
    raise err

finally:
    self.database.close()
