from flask import jsonify
from werkzeug.exceptions import MethodNotAllowed, NotFound

from . import app


@app.errorhandler(NotFound)
def handle_method_not_allowed(error):
    response = jsonify({
        'error_code': 'http_not_found',
        'error_message': error.description
    })
    response.status_code = error.code
    return response


@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(error):
    response = jsonify({
        'error_code': 'http_method_not_allowed',
        'error_message': error.description
    })
    response.status_code = error.code
    return response
