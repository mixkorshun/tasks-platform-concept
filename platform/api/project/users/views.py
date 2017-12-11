from flask import request, jsonify
from werkzeug.exceptions import NotFound

from project import app
from project.auth.shortcuts import only_authorized
from project.users.models import get_by_id


@app.route('/users/me/', methods=['GET'])
@only_authorized
def profile():
    user = get_by_id(request.session.user_id)

    if not user:
        raise NotFound(
            'Current user not found in database.'
        )

    return jsonify(user)
