from flask_restful import Resource
from flask import request
from api.token import check_token
from api.http_header import build_response_header_extract_user_email
from dbModels.userModel import UserModel

# Routes permettant d'obtenir les choix pour le cold start (liste des topics id)
# et de sauvegarder le choix de l'utilisateur.
# Ne retourne aucune recommandations !!!
from flask import send_file


class ConsentFormAPI(Resource):

    _model = UserModel()

    # @check_token()
    # def get(self):
    #     email = request.args.get('user_id')
    #     user = UserModel.query.filter_by(email=email).first()
    #     response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '),
    #                                                         data=user.fic_acceptance)
    #     return response

    @check_token()
    def post(self):
        response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '))
        res = request.get_json()
        print(res)
        self._model.save_fic_acceptance(acceptance=res['acceptance'], email=email)
        return response




