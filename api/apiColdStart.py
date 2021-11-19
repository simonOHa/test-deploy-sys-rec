from flask_restful import Resource, request
from dbModels.sysRecColdStartModel import SysRecColdStartModel

# Routes permettant d'obtenir les choix pour le cold start (liste des topics id)
# et de sauvegarder le choix de l'utilisateur.
# Ne retourne aucune recommandations !!!


class ColdStartAPI(Resource):

    _model = SysRecColdStartModel()

    def get(self):
        choices = self._model.get_cold_start_choices()
        return {'choices': choices.tolist()}, 200

    def post(self):
        res = request.get_json()
        return self._model.save_cold_start_choice(cold_start_choice=res['result'], user_id=res['user_id']), 200


