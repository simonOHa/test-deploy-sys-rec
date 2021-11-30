from flask import jsonify, make_response
from dbModels.userModel import UserModel

def buid_response_header_get(access_token, data):
    user = UserModel.query.filter_by(access_token=access_token).first()
    response = make_response(jsonify(data),200)
    response.headers["Content-Type"] = "application/json"
    response.headers["Authorization"] = 'Bearer ' + user.access_token
    return response


def buid_response_header_post(access_token):
    user = UserModel.query.filter_by(access_token=access_token).first()
    response = make_response('',200)
    response.headers["Content-Type"] = "application/json"
    response.headers["Authorization"] = 'Bearer ' + user.access_token

    return (response, user.email)