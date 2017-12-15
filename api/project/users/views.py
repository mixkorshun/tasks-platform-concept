import simplejson
from flask import request, jsonify
from werkzeug.exceptions import NotFound, BadRequest

from project import app
from project.utils import validators as v
from . import tokens, actions
from .models import get_user_by_id
from .shortcuts import only_authorized


@app.route('/users/me/', methods=['GET'])
@only_authorized
def users_me():
    user = get_user_by_id(request.user_id)

    if not user:
        raise NotFound(
            'User not found in database.'
        )

    del user['password']

    return jsonify(user)


@app.route('/users/login/', methods=['POST'])
def users_login():
    post_data = simplejson.loads(request.data.decode())

    try:
        email = v.email(v.required(post_data['email']))
        password = v.required(post_data['password'])
    except (KeyError, ValueError):
        raise BadRequest(
            'Please provide email/password pair.'
        )

    try:
        user = actions.login(email, password)
    except LookupError:
        resp = jsonify({
            'error_code': 'invalid_credentials',
            'error_message': 'Incorrect email or password.'
        })
        resp.status_code = 400

        return resp

    token = tokens.get_token(request, user['id'])

    return jsonify({
        'token': token
    })


@app.route('/users/register/', methods=['POST'])
def users_register():
    post_data = simplejson.loads(request.data.decode())

    try:
        email = v.email(v.required(post_data['email']))
        password = v.required(post_data['password'])
        user_type = v.choices(post_data['type'], ('employer', 'employee'))
    except (KeyError, ValueError):
        raise BadRequest('Invalid form params.')

    user = actions.register(
        email=email,
        password=password,
        type=user_type
    )

    del user['password']

    return jsonify(user)
