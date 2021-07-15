import logging
import traceback
from flask import abort
from datetime import datetime
from db.database import Database
from admin.admin_dao import AdminDao

class AdminService:
    def __init__(self):
        self.admin_dao = AdminDao()
        self.database = Database()

    def admin_signup(self, data):
        try:
            # reqeust data 확인
            if not data:
                return abort(400, description="INVALID_DATA")

            # 기존 admin 정보 확인
            select_admin_query = self.admin_dao.select_admin(data)
            admin_info = self.database.execute(select_admin_query).fetchone()
            if admin_info:
                return abort(400, description="EXISTS_ADMIN")

            validate_keys = [
                'admin_class_cd'
                , 'email'
                , 'password'
            ]
            for key in validate_keys:
                if key not in data:
                    return abort(400, description="INVALID_KEYS")

            param_data = dict()

            if len(data['email'].strip()) == 0:
                return abort(400, description="INVALID_DATA")

            if len(data['password'].strip()) == 0:
                return abort(400, description="INVALID_DATA")

            if len(data['admin_class_cd'].strip()) == 0:
                return abort(400, description="INVALID_DATA")

            if len(data['admin_grade_cd'].strip()) == 0:
                return abort(400, description="INVALID_DATA")

            param_data['regist_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            param_data['update_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            param_data['is_use'] = 'Y'

            # start transaction
            self.database.start_transaction()

            # get admin_id
            get_admin_id_query = self.admin_dao.get_admin_id()
            admin_id_info = self.database.execute(get_admin_id_query).fetchone()
            param_data['admin_id'] = admin_id_info['admin_id']

            # insert admin query
            insert_admin_query = self.admin_dao.insert_admin()
            self.database.execute(insert_admin_query, param_data)

            # commit
            self.database.commit()

            return True

        except Exception as err:
            error_message = 'Exception execute Error ( {} )'.format(hasattr(err, 'message') and err.message or err)
            logging.error(error_message)
            error_info = 'Exception Error info ( {} )'.format(traceback.format_exc())
            logging.error(error_info)
            raise err

        finally:
            self.database.close()
