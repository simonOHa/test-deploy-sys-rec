from flask_restful import Resource
from flask import request
from dbModels.globalCommentModel import GlobalCommentModel
from api.token import check_token
from api.http_header import build_response_header
from api.errors import InternalServerError
from dbModels.userModel import UserModel


class GlobalCommentAPI(Resource):

    _model = GlobalCommentModel()

    @check_token()
    def get(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ','')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            _comment_model = GlobalCommentModel.query.filter_by(email=_user.email).first()

            if _comment_model is not None:
                response = build_response_header(access_token=_access_token, status_code=200,
                                                 data=_comment_model.comment, error_message=None)
            else:
                response = build_response_header(access_token=_access_token, status_code=200, data=None, error_message=None)
            return response



        except Exception as e:
            raise InternalServerError

    @check_token()
    def post(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ','')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            _request = request.get_json()
            self._model.save_comment(comment=_request['result'], email=_user.email)
            response = build_response_header(access_token=_access_token, status_code=200, data=None, error_message=None)
            return response

        except Exception as e:
            raise InternalServerError