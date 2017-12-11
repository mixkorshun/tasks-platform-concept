from flask import jsonify
from werkzeug.exceptions import MethodNotAllowed, NotFound, Forbidden, \
    BadRequest

from . import app


@app.errorhandler(NotFound)
def handle_not_found(error):
    response = jsonify({
        'error_code': 'not_found',
        'error_message': error.description
    })
    response.status_code = error.code
    return response


@app.errorhandler(BadRequest)
def handle_bad_request(error):
    response = jsonify({
        'error_code': 'bad_request',
        'error_message': error.description
    })
    response.status_code = error.code
    return response


@app.errorhandler(Forbidden)
def handle_forbidden(error):
    response = jsonify({
        'error_code': 'not_allowed',
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
