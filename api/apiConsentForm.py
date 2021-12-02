from flask_restful import Resource
from dbModels.consentFormModel import ConsentFormModel
from api.token import check_token
from api.http_header import buid_response_header_get,buid_response_header_post
from flask import jsonify, make_response, request, Response
from dbModels.userModel import UserModel
# Routes permettant d'obtenir les choix pour le cold start (liste des topics id)
# et de sauvegarder le choix de l'utilisateur.
# Ne retourne aucune recommandations !!!
from flask import send_file

class ConsentFormAPI(Resource):

    _model = ConsentFormModel()

    @check_token()
    def get(self):
        email = request.args.get('user_id')
        user_consent_form = ConsentFormModel.query.filter_by(email=email).first()
        response = buid_response_header_get(access_token=request.headers['Authorization'].strip('Bearer '),
                                            data=user_consent_form.acceptance)
        return response

    @check_token()
    def post(self):
        response, email = buid_response_header_post(access_token=request.headers['Authorization'].strip('Bearer '))
        res = request.get_json()
        self._model.save_consentForm(acceptance=res['acceptance'], email=email)
        return response




