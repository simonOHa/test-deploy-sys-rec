from flask_restful import Resource, request
from dbModels.sysRecUserAreaInterest import SysRecUserAreaInterest
from flask import jsonify

class UserInterestAreaAPI(Resource):

    _model = SysRecUserAreaInterest()

    def get(self):
        user_id = request.args.get('user_id')
        area_interest = self._model.get_user_area_interest(user_id)
        return area_interest, 200




