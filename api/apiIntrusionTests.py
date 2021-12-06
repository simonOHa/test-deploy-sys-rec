from flask_restful import Resource
from flask import request
from dbModels.intrusionTestModels import IntrusionTestWSIModel, IntrusionTestTIModel, IntrusionTestWIModel
from api.token import check_token
from api.http_header import build_response_header_extract_user_email


class IntrusionTestTIAPI(Resource):

    _model = IntrusionTestTIModel()

    @check_token()
    def get(self):
        response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '),
                                                            data=self._model.read_ti_data())
        return response

    @check_token()
    def post(self):
        response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '))
        res = request.get_json()
        self._model.save_to_db(res, email)
        return response


class ResultsIntrusionTestTIAPI(Resource):

    _model = IntrusionTestTIModel()

    @check_token()
    def get(self):
        email = request.args.get('user_id')
        user_intrusion_test = IntrusionTestTIModel.query.filter_by(email=email).first()
        if user_intrusion_test is None:
            response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '))
        else:
            response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '),
                                                                       data=user_intrusion_test.result_candidate_value)
        return response


class IntrusionTestWIAPI(Resource):

    _model = IntrusionTestWIModel()

    @check_token()
    def get(self):
        response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '),
                                                            data=self._model.read_wi_data())
        return response

    @check_token()
    def post(self):
        response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '))
        res = request.get_json()
        self._model.save_to_db(res, email)
        return response


class ResultsIntrusionTestWIAPI(Resource):

    _model = IntrusionTestWIModel()

    @check_token()
    def get(self):
        email = request.args.get('user_id')
        user_intrusion_test = IntrusionTestWIModel.query.filter_by(email=email).first()

        if user_intrusion_test is None:
            response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '))
        else:
            response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '),
                                                                        data=user_intrusion_test.result)
        return response


class IntrusionTestWSIAPI(Resource):

    _model = IntrusionTestWSIModel()

    @check_token()
    def get(self):
        response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '),
                                                            data=self._model.read_wsi_data())
        return response

    @check_token()
    def post(self):
        response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '))
        res = request.get_json()
        self._model.save_to_db(res, email)
        return response


class ResultsIntrusionTestWSIAPI(Resource):

    _model = IntrusionTestWSIModel()

    @check_token()
    def get(self):
        email = request.args.get('user_id')
        user_intrusion_test = IntrusionTestWSIModel.query.filter_by(email=email).first()

        if user_intrusion_test is None:
            response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '))
        else:
            response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '),
                                                                        data=user_intrusion_test.result)
        return response

