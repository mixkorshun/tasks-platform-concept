import json

from flask import request, jsonify

from project import app
from project.users.models import get_user_by_credentials, make_user, \
    create_user
from project.users.password import encode_password
from . import tokens
from .errors import InvalidCredentials


@app.route('/authorize/', methods=['POST'])
def authorize():
    post_data = json.loads(request.data.decode())

    email = post_data['email']
    password = post_data['password']

    user = get_user_by_credentials(email, password)

    if not user:
        raise InvalidCredentials()

    token = tokens.get_token(user['id'])

    return jsonify({
        'token': token
    })


@app.route('/register/', methods=['POST'])
def register():
    post_data = json.loads(request.data.decode())

    email = post_data['email']
    password = post_data['password']
    user_type = post_data['type']

    user = create_user(make_user(
        email=email,
        password=encode_password(password),
        type=user_type
    ))

    del user['password']

    return jsonify(user)


@app.errorhandler(InvalidCredentials)
def handle_invalid_credentials(error):
    response = jsonify({
        'error_code': error.code,
        'error_message': error.message
    })
    response.status_code = 400

    return response
