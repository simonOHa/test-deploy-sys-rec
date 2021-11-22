from flask_restful import Resource, request
from dbModels.sysRecColdStartModel import SysRecColdStartModel
from flask_cors import cross_origin
# Routes permettant d'obtenir les choix pour le cold start (liste des topics id)
# et de sauvegarder le choix de l'utilisateur.
# Ne retourne aucune recommandations !!!


class ColdStartAPI(Resource):

    _model = SysRecColdStartModel()

    @cross_origin(allow_headers=['Content-Type'])
    def get(self):
        choices = self._model.get_cold_start_choices()
        return {'choices': choices.tolist()}, 200

    @cross_origin(allow_headers=['Content-Type'])
    def post(self):
        res = request.get_json()
        return self._model.save_cold_start_choice(cold_start_choice=res['result'], user_id=res['user_id']), 200


