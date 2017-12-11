from flask import request, jsonify
from werkzeug.exceptions import NotFound

from project import app
from project.auth.shortcuts import only_authorized
from .models import get_user_by_id


@app.route('/users/me/', methods=['GET'])
@only_authorized
def users_me():
    return users_detail(request.session.user_id)


@app.route('/users/<int:user_id>/', methods=['GET'])
def users_detail(user_id):
    user = get_user_by_id(user_id)

    if not user:
        raise NotFound(
            'User not found in database.'
        )

    del user['password']

    return jsonify(user)
