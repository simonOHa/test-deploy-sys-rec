from flask_restful import Resource
from flask import request
from api.token import check_token
from api.http_header import build_response_header
from dbModels.userModel import UserModel
from api.errors import InternalServerError

# Routes permettant d'obtenir les choix pour le cold start (liste des topics id)
# et de sauvegarder le choix de l'utilisateur.
# Ne retourne aucune recommandations !!!
from flask import send_file


class ConsentFormAPI(Resource):

    @check_token()
    def post(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ','')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            _request = request.get_json()
            UserModel().save_fic_acceptance(acceptance=_request['acceptance'], email=_user.email)
            response = build_response_header(access_token=_access_token, status_code=200, data=None, error_message=None)
            return response

        except Exception as e:
            raise InternalServerError




