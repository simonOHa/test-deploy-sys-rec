from flask_restful import Resource
from dbModels.userModel import UserModel
from flask_cors import cross_origin


class UserAPI(Resource):

    _model = UserModel()

    @cross_origin()
    def __init__(self):
        pass

    @cross_origin()
    def get(self):
        return {"id": self._model.generate_user_id()}, 200