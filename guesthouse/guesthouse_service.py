import logging
import traceback
from flask import abort
from datetime import datetime
from db.database import Database
from admin.admin_dao import AdminDao
from guesthouse.guesthouse_dao import guesthouseDao


class SpaceService:
    def __init__(self):
        self.database = Database()
        self.admin_dao = AdminDao()
        self.guesthouse_dao = guesthouseDao()

    def guesthouse_create(self, data):
        try:
            # request data 검증
            if not data:
                return abort(400, description="INVALID_DATA")
            validate_keys = [
                , 'name'
                , 'location_info'
                , 'free'
                , 'price'
                , 'information'
                , 'use_time'
                , 'use_step'
                , 'use_price'
                , 'space_images'
                , 'is_post'
            ]
            for key in validate_keys:
                if key not in data:
                    return abort(400, description="INVALID_KEYS")

            param_data = dict()
            if len(data['space_class_cd'].strip()) == 0:
                return abort(400, description="INVALID_DATA")
            if len(data['space_class_cd'].strip()) > 0:
                param_data['space_class_cd'] = data['space_class_cd']

            if len(data['is_post'].strip()) == 0:
                return abort(400, description="INVALID_DATA")
            param_data['is_post'] = data['is_post']

            if len(data['name'].strip()) == 0:
                return abort(400, description="INVALID_DATA")
            param_data['name'] = data['name']

            if len(data['location_info'].strip()) == 0:
                return abort(400, description="INVALID_DATA")
            param_data['location_info'] = data['location_info']

            if len(data['information'].strip()) == 0:
                return abort(400, description="INVALID_DATA")
            param_data['information'] = data['information']

            if len(data['use_time'].strip()) == 0:
                return abort(400, description="INVALID_DATA")
            param_data['use_time'] = data['use_time']

            if len(data['use_step'].strip()) == 0:
                return abort(400, description="INVALID_DATA")
            param_data['use_step'] = data['use_step']

            if len(data['use_price'].strip()) == 0:
                return abort(400, description="INVALID_DATA")
            param_data['use_price'] = data['use_price']

            if len(data['free'].strip()) == 0:
                return abort(400, description="INVALID_DATA")
            if len(data['free']) > 0:
                param_data['free'] = data['free']

            if len(data['price'].strip()) == 0:
                return abort(400, description="INVALID_DATA")
            if len(data['price']) > 0:
                param_data['price'] = int(data['price'])

            # 공간 이미지 validate
            space_image_insert_count = 0 if data['space_images'][0].filename == '' else len(data['space_images'])
            if space_image_insert_count == 0:
                return abort(400, description="INVALID_DATA")
            if space_image_insert_count > 5:
                return abort(400, description="TOO_MANY_IMAGES")

            param_data['regist_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            param_data['update_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # start transaction
            self.database.start_transaction()

            # get space id
            get_guesthouse_id_query = self.guesthouse_dao.get_guesthouse_id()
            guesthouse_id_info = self.database.execute(get_guesthouse_id_query).fetchone()
            param_data['guesthouse_id'] = guesthouse_id_info['guesthouse_id']
            guesthouse_id = guesthouse_id_info['space_id']

            # get space_image id
            get_space_image_id_query = self.space_dao.get_space_image_id()

            # S3 upload space_image and insert space_image
            if space_image_insert_count > 0:
                # insert space_image
                insert_space_image_query = self.space_dao.insert_space_image()
                for file in data['space_images']:
                    # S3 upload space_image
                    upload_location = f'SPACE/{space_id}'
                    space_image_url = self.aws_s3_manager.upload_s3(file, upload_location)

                    space_image_id_info = self.database.execute(get_space_image_id_query).fetchone()
                    space_image_param_data = dict()
                    space_image_param_data['space_image_id'] = space_image_id_info['space_image_id']
                    space_image_param_data['space_id'] = space_id_info['space_id']
                    space_image_param_data['location'] = space_image_url
                    space_image_param_data['regist_date'] = param_data['regist_date']
                    space_image_param_data['update_date'] = param_data['update_date']
                    self.database.execute(insert_space_image_query, space_image_param_data)

            # select first space_image_id
            main_space_image_param_data = dict()
            main_space_image_param_data['space_id'] = space_id_info['space_id']
            main_space_image_param_data['order_by'] = 'ASC'
            main_space_image_param_data['is_use'] = 'Y'
            select_space_image_query = self.space_dao.select_space_image(main_space_image_param_data)
            main_space_image_info = self.database.execute(select_space_image_query).fetchone()

            # insert space
            param_data['master_admin_id'] = admin_info['T101_admin_id']
            param_data['main_image_id'] = main_space_image_info['T101_space_image_id']
            param_data['space_id'] = space_id_info['space_id']
            param_data['stock'] = None
            insert_space_query = self.space_dao.insert_space()
            self.database.execute(insert_space_query, param_data)
            print(param_data)
            # insert space price query
            insert_space_price_query = self.space_dao.insert_space_price()
            self.database.execute(insert_space_price_query, param_data)

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
