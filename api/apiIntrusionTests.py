from flask_restful import Resource, request
from dbModels.intrusionTestModels import ResultsIntrusionTestWSI, ResultsIntrusionTestTI, ResultsIntrusionTestWI


class ResultsIntrusionTestTI(Resource):

    _model = ResultsIntrusionTestTI()

    def get(self):

        return self._model.read_ti_data()

    def post(self):
        res = request.get_json()
        return self._model.save_to_db(self._model, res), 200


class ResultsIntrusionTestWI(Resource):

    _model = ResultsIntrusionTestWI()

    def get(self):
        return self._model.read_wi_data()


    def post(self):
        res = request.get_json()
        return self._model.save_to_db(self._model, res), 200


class ResultsIntrusionTestWSI(Resource):

    _model = ResultsIntrusionTestWSI()

    def get(self):
        return self._model.read_wsi_data()

    def post(self):
        res = request.get_json()
        return self._model.save_to_db(self._model, res), 200


