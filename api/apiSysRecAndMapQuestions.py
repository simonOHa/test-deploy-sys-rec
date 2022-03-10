from flask_restful import Resource
from flask import request
from api.token import check_token
from api.http_header import build_response_header
from dbModels.sysRecAndMapQuestions import SysRecAndMapQuestionsModel
from dbModels.userModel import UserModel
from api.errors import InternalServerError


class SysRecAndMapQuestionsAPI(Resource):

    _model = SysRecAndMapQuestionsModel()

    @check_token()
    def get(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ', '')
            _user = UserModel.query.filter_by(access_token=_access_token).first()

            _data = self._model.get_questions(email=_user.email)
            response = build_response_header(access_token=_access_token,
                                             status_code=200,
                                             data=_data,
                                             error_message=None)
            return response

        except Exception as e:
            raise InternalServerError

    def post(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ', '')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            _request = request.get_json()
            SysRecAndMapQuestionsModel().save_to_db(results=_request['results'], email=_user.email)
            response = build_response_header(access_token=_access_token, status_code=200, data=None, error_message=None)
            return response

        except Exception as e:
            raise InternalServerError


