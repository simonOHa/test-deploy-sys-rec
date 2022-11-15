from flask_restful import Resource
from flask import request
from dbModels.sysRecColdStartModel import SysRecColdStartModel
from api.token import check_token
from api.http_header import build_response_header

# Routes permettant d'obtenir les choix pour le cold start (liste des topics id)
# et de sauvegarder le choix de l'utilisateur.
# Ne retourne aucune recommandations !!!
from dbModels.userModel import UserModel
from api.errors import InternalServerError


class ColdStartAPI(Resource):

    @check_token()
    def get(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ','')
            _data = SysRecColdStartModel().get_cold_start_choices()
            response = build_response_header(access_token=_access_token, status_code=200, data=_data, error_message=None)
            return response

        except Exception as e:
            raise InternalServerError

    @check_token()
    def post(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ','')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            _request = request.get_json()
            SysRecColdStartModel().save_cold_start_choice(cold_start_choice=_request['result'], email=_user.email)
            response = build_response_header(access_token=_access_token, status_code=200, data=None, error_message=None)
            return response

        except Exception as e:
            raise InternalServerError


class ResultColdStartAPI(Resource):
    @check_token()
    def get(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ','')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            _user_cold_start = SysRecColdStartModel.query.filter_by(email=_user.email).first()

            if _user_cold_start is not None:
                response = build_response_header(access_token=_access_token, status_code=200, data=_user_cold_start.cold_start_position, error_message=None)
            else:
                response = build_response_header(access_token=_access_token, status_code=200, data=None, error_message=None)
            return response

        except Exception as e:
            raise InternalServerError




