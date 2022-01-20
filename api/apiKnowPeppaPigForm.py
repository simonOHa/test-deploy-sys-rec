from flask_restful import Resource
from flask import request
from api.token import check_token
from api.http_header import build_response_header
from dbModels.userModel import UserModel
from api.errors import InternalServerError


class KnowPeppaPigFormAPI(Resource):

    _model = UserModel()

    @check_token()
    def post(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ','')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            _request = request.get_json()
            self._model.save_know_peppa_pig(know_peppa_pig=_request['know_peppa_pig'], email=_user.email)
            response = build_response_header(access_token=_access_token, status_code=200, data=None, error_message=None)
            return response

        except Exception as e:
            raise InternalServerError




