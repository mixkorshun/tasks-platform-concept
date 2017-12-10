import json

from flask import request, jsonify

from project import app
from project.session import Store, to_jwt_token
from .errors import InvalidCredentials
from .models import get_by_credentials


@app.route('/users/authorize/', methods=['POST'])
def authorize():
    post_data = json.loads(request.data.decode())

    email = post_data['email']
    password = post_data['password']

    user = get_by_credentials(email, password)

    if not user:
        raise InvalidCredentials()

    token = to_jwt_token(Store(
        user_id=user.id
    ))

    return jsonify({
        'token': token
    })


@app.errorhandler(InvalidCredentials)
def handle_invalid_credentials(error):
    response = jsonify({
        'error_code': error.code,
        'error_message': error.message
    })
    response.status_code = 400

    return response
