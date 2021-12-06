from flask import jsonify, make_response
from dbModels.userModel import UserModel


def build_response_header_extract_user_email(access_token, data=None):
    user = UserModel.query.filter_by(access_token=access_token).first()
    if data is None:
        response = make_response('', 200)
    else:
        response = make_response(jsonify(data),200)

    response.headers["Content-Type"] = "application/json"
    response.headers["Authorization"] = 'Bearer ' + user.access_token

    return (response, user.email)


# def build_response_header_without_data(access_token):
#     user = UserModel.query.filter_by(access_token=access_token).first()
#     response = make_response('',200)
#     response.headers["Content-Type"] = "application/json"
#     response.headers["Authorization"] = 'Bearer ' + user.access_token
#
#     return (response, user.email)