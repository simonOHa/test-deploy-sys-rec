from flask_restful import Resource
from flask import request
from api.token import check_token
from api.http_header import build_response_header
from dbModels.sysRecSemanticMapQuestionsModel import SysRecSemanticMapQuestionsModel
from dbModels.userModel import UserModel
from api.errors import InternalServerError


class SemanticMapQuestionsAPI(Resource):

    _model = SysRecSemanticMapQuestionsModel()

    @check_token()
    def get(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ', '')
            response = build_response_header(access_token=_access_token, status_code=200, data=self._model.get_questions(), error_message=None)
            return response

        except Exception as e:
            raise InternalServerError

    def post(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ', '')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            _request = request.get_json()
            SysRecSemanticMapQuestionsModel().save_to_db(results=_request['results'], email=_user.email)
            response = build_response_header(access_token=_access_token, status_code=200, data=None, error_message=None)
            return response

        except Exception as e:
            raise InternalServerError


class SemanticMapQuestionsResultsAPI(Resource):

    _model = SysRecSemanticMapQuestionsModel()

    @check_token()
    def get(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ', '')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            user_open_questions = SysRecSemanticMapQuestionsModel.query.filter_by(email=_user.email).first()
            if user_open_questions is not None:
                results = {'question_1': user_open_questions.question_1,
                           'question_2': user_open_questions.question_2,
                           'question_3': user_open_questions.question_3,
                           'question_4': user_open_questions.question_4
                           }
                response = build_response_header(access_token=_access_token, status_code=200, data=results, error_message=None)
            else:
                response = build_response_header(access_token=_access_token, status_code=200, data=None, error_message=None)

            return response

        except Exception as e:
            raise InternalServerError

