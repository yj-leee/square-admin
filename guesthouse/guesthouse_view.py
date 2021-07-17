from flask import request
from flask import jsonify
from flask import current_app


def create_endpoint(app, services):
    guesthouse_service = services.guesthouse_service

    @app.route("/space/insert", methods=['POST'])
    def create_guesthouse():
        if request.method == 'POST':
            current_app.logger.info('request form data :{}'.format(request.form.to_dict()))
            current_app.logger.info('request files :{}'.format(request.files))
            data = request.form.to_dict()
            data.update(request.files.to_dict(flat=False))
            guesthouse_service.guesthouse_create(data)

            return jsonify({'message': "SUCCESS"})
