from flask_restful import Resource
from flask import request
from api.token import check_token
from api.http_header import build_response_header
from dbModels.sysRecPredilectionTermModel import SysRecPredilectionTermModel
from dbModels.userModel import UserModel
from api.errors import InternalServerError


class PredilectionTermAPI(Resource):

    #_model = SysRecPredilectionTermModel()

    @check_token()
    def get(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ', '')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            _predilection_model = SysRecPredilectionTermModel.query.filter_by(email=_user.email).first()

            if _predilection_model is not None:
                response = build_response_header(access_token=_access_token, status_code=200,
                                                 data=_predilection_model.predilection_term, error_message=None)
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
            SysRecPredilectionTermModel().save_predilection_term(predilection_term=_request['result'], email=_user.email)
            response = build_response_header(access_token=_access_token, status_code=200, data=None, error_message=None)
            return response

        except Exception as e:
            raise InternalServerError
