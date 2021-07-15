import logging
import traceback

class AdminDao:
    def get_admin_id(self):
        try:
            get_admin_id_query = (
                """
                SELECT @admin_id := fn_get_seq_8('ADMI') AS admin_id
                """
            )

            return get_admin_id_query

        except Exception as err:
            error_message = 'Exception database Error ( {} )'.format(hasattr(err, 'message') and err.message or err)
            logging.error(error_message)
            error_info = 'Exception Error info ( {} )'.format(traceback.format_exc())
            logging.error(error_info)
            raise err

    def select_admin(self, param_data):
        try:
            select_admin_query = (
                """
                SELECT T101.admin_id 
                FROM  tb_admin AS T101
                WHERE  1=1
                """
            )
            if 'email' in param_data:
                email = "\'" + str(param_data['email']) + "\'"
                select_admin_query += f' AND T101.email = {email}'

            return select_admin_query

        except Exception as err:
            error_message = 'Exception database Error ( {} )'.format(hasattr(err, 'message') and err.message or err)
            logging.error(error_message)
            error_info = 'Exception Error info ( {} )'.format(traceback.format_exc())
            logging.error(error_info)
            raise err

    def insert_admin(self):
        try:
            insert_admin_query = (
                """
                INSERT INTO tb_admin
                (
                    admin_id 
                    ,email
                    ,password
                    ,admin_status_cd
                    ,admin_grade_cd
                    ,regist_date
                    ,update_date
                    ,is_use
                ) VALUES 
                (
                    %(admin_id)s
                    ,%(email)s
                    ,%(password)s
                    ,%(admin_status_cd)s
                    ,%(admin_grade_cd)s
                    ,%(regist_date)s
                    ,%(update_date)s
                    ,%(is_use)s
                )
            """
            )

            return insert_admin_query

        except Exception as err:
            error_message = 'Exception database Error ( {} )'.format(hasattr(err, 'message') and err.message or err)
            logging.error(error_message)
            error_info = 'Exception Error info ( {} )'.format(traceback.format_exc())
            logging.error(error_info)
            raise err