from flask import request
from flask import jsonify
from flask import current_app




class AdminView:
    def create_endpoint(app, services):
        admin_service = services.admin_service

        @app.errorhandler(400)
        def http_400_bad_request(error):
            response = jsonify({'message': error.description})
            response.status_code = 400
            current_app.logger.error('error_info: {}'.format(error))
            current_app.logger.error('error_info: {}'.format(response))
            return response

        @app.errorhandler(401)
        def http_401_unauthorized(error):
            response = jsonify({'message': error.description})
            response.status_code = 401
            current_app.logger.error('error_info: {}'.format(error))
            current_app.logger.error('error_info: {}'.format(response))
            return response

        @app.errorhandler(404)
        def http_404_not_found(error):
            response = jsonify({'message': "INVALID_URL"})
            response.status_code = 404
            current_app.logger.error('error_info: {}'.format(error))
            current_app.logger.error('error_info: {}'.format(response))
            return response

        @app.route("/admin/signup", methods=['POST'])
        def admin_signup():
            current_app.logger.info('request :{}'.format(request))
            current_app.logger.info('request data :{}'.format(request.json))
            data = request.json
            admin_service.admin_signup(data)

            return jsonify({'message': "SUCCESS"})