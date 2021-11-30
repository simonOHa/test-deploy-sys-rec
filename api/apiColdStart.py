from flask_restful import Resource, request
from dbModels.sysRecColdStartModel import SysRecColdStartModel
from api.token import check_token
from api.http_header import buid_response_header_get,buid_response_header_post

# Routes permettant d'obtenir les choix pour le cold start (liste des topics id)
# et de sauvegarder le choix de l'utilisateur.
# Ne retourne aucune recommandations !!!


class ColdStartAPI(Resource):

    _model = SysRecColdStartModel()

    @check_token()
    def get(self):
        response = buid_response_header_get(access_token=request.headers['Authorization'].strip('Bearer '),
                                            data=self._model.get_cold_start_choices())
        return response

    @check_token()
    def post(self):
        response, email = buid_response_header_post(access_token=request.headers['Authorization'].strip('Bearer '))
        res = request.get_json()
        self._model.save_cold_start_choice(cold_start_choice=res['result'], email=email)
        return response




