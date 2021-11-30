from flask_restful import Resource, request
from dbModels.intrusionTestModels import ResultsIntrusionTestWSI, ResultsIntrusionTestTI, ResultsIntrusionTestWI
from api.token import check_token
from api.http_header import buid_response_header_get,buid_response_header_post


class ResultsIntrusionTestTI(Resource):

    _model = ResultsIntrusionTestTI()

    @check_token()
    def get(self):
        response = buid_response_header_get(access_token=request.headers['Authorization'].strip('Bearer '),
                                            data=self._model.read_ti_data())
        return response

    @check_token()
    def post(self):
        response, email = buid_response_header_post(access_token=request.headers['Authorization'].strip('Bearer '))
        res = request.get_json()
        self._model.save_to_db(self._model, res, email)
        return response


class ResultsIntrusionTestWI(Resource):

    _model = ResultsIntrusionTestWI()

    @check_token()
    def get(self):
        response = buid_response_header_get(access_token=request.headers['Authorization'].strip('Bearer '),
                                            data=self._model.read_wi_data())
        return response

    @check_token()
    def post(self):
        response, email = buid_response_header_post(access_token=request.headers['Authorization'].strip('Bearer '))
        res = request.get_json()
        self._model.save_to_db(self._model, res, email)
        return response


class ResultsIntrusionTestWSI(Resource):

    _model = ResultsIntrusionTestWSI()

    @check_token()
    def get(self):
        response = buid_response_header_get(access_token=request.headers['Authorization'].strip('Bearer '),
                                            data=self._model.read_wsi_data())
        return response

    @check_token()
    def post(self):
        response, email = buid_response_header_post(access_token=request.headers['Authorization'].strip('Bearer '))
        res = request.get_json()
        self._model.save_to_db(self._model, res, email)
        return response


