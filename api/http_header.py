from flask import jsonify, make_response
from werkzeug.http import HTTP_STATUS_CODES


def build_response_header(access_token, status_code, data=None, error_message=None):
    if error_message is not None:
        response = make_response({'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')})
    elif data is None:
        response = make_response('')
    else:
        response = make_response(jsonify(data))

    response.headers["Content-Type"] = "application/json"
    response.headers["Authorization"] = 'Bearer ' + access_token
    response.status_code = status_code

    return response

