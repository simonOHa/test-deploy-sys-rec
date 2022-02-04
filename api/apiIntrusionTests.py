from flask_restful import Resource
from flask import request
from dbModels.intrusionTestModels import IntrusionTestWSIModel, IntrusionTestTIModel, IntrusionTestWIModel
from api.token import check_token
from api.http_header import build_response_header
from dbModels.userModel import UserModel
from api.errors import InternalServerError


class IntrusionTestScore(Resource):
    _ti_model = IntrusionTestTIModel()
    _wi_model = IntrusionTestWIModel()
    _wsi_model = IntrusionTestWSIModel()

    @check_token()
    def get(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ', '')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            _data = {}

            _user_ti = self._ti_model.query.filter_by(email=_user.email).first()
            if _user_ti is not None:
                _data['ti_score'] = _user_ti.score

            _user_wi = self._wi_model.query.filter_by(email=_user.email).first()
            if _user_wi is not None:
                _data['wi_score'] = _user_wi.score

            _user_wsi = self._wsi_model.query.filter_by(email=_user.email).first()
            if _user_wsi is not None:
                _data['wsi_score'] = _user_wsi.score

            response = build_response_header(access_token=_access_token, status_code=200, data=_data, error_message=None)
            return response
        except Exception as e:
            raise InternalServerError


class IntrusionTestTIAPI(Resource):

    _model = IntrusionTestTIModel()

    @check_token()
    def get(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ', '')
            _results = self._model.read_ti_data()
            response = build_response_header(access_token=_access_token, status_code=200, data=_results, error_message=None)
            return response
        except Exception as e:
            raise InternalServerError

    @check_token()
    def post(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ', '')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            _request = request.get_json()
            self._model.save_to_db(_request, _user.email)
            response = build_response_header(access_token=_access_token, status_code=200, data=None, error_message=None)
            return response
        except Exception as e:
            raise InternalServerError


class ResultsIntrusionTestTIAPI(Resource):

    _model = IntrusionTestTIModel()

    @check_token()
    def get(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ', '')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            _user_intrusion_test = IntrusionTestTIModel.query.filter_by(email=_user.email).first()

            if _user_intrusion_test is None:
                response = build_response_header(access_token=_access_token, status_code=200, data=None, error_message=None)
            else:
                _questions = _user_intrusion_test.question
                _results_candidate_id = _user_intrusion_test.result_candidate_id
                _results_candidate_value = _user_intrusion_test.result_candidate_value
                _results_video_watched_extra_info = _user_intrusion_test.video_watched_extra_info

                answer = []
                for i in range(len(_questions)):
                    answer.append({
                        'question': _questions[i],
                        'candidate_id': _results_candidate_id[i],
                        'candidate_value': _results_candidate_value[i],
                        'video_watched_extra_info': _results_video_watched_extra_info[i]
                    })

                response = build_response_header(access_token=_access_token, status_code=200,data=answer, error_message=None)


            return response
        except Exception as e:
            raise InternalServerError


class IntrusionTestWIAPI(Resource):

    _model = IntrusionTestWIModel()

    @check_token()
    def get(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ', '')
            _results = self._model.read_wi_data()
            response = build_response_header(access_token=_access_token, status_code=200, data=_results, error_message=None)
            return response

        except Exception as e:
            raise InternalServerError

    @check_token()
    def post(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ','')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            _request = request.get_json()
            self._model.save_to_db(_request, _user.email)
            response = build_response_header(access_token=_access_token, status_code=200, data=None, error_message=None)
            return response

        except Exception as e:
            raise InternalServerError


class ResultsIntrusionTestWIAPI(Resource):

    _model = IntrusionTestWIModel()

    @check_token()
    def get(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ','')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            _user_intrusion_test = IntrusionTestWIModel.query.filter_by(email=_user.email).first()

            if _user_intrusion_test is None:
                response = build_response_header(access_token=_access_token, status_code=200, data=None, error_message=None)
            else:
                response = build_response_header(access_token=_access_token, status_code=200, data=_user_intrusion_test.result, error_message=None)

            return response
        except Exception as e:
            raise InternalServerError


class IntrusionTestWSIAPI(Resource):

    _model = IntrusionTestWSIModel()

    @check_token()
    def get(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ','')
            _results = self._model.read_wsi_data()
            response = build_response_header(access_token=_access_token, status_code=200, data=_results, error_message=None)
            return response

        except Exception as e:
            raise InternalServerError

    @check_token()
    def post(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ','')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            _request = request.get_json()
            self._model.save_to_db(_request, _user.email)
            response = build_response_header(access_token=_access_token, status_code=200, data=None, error_message=None)
            return response
        except Exception as e:
            raise InternalServerError


class ResultsIntrusionTestWSIAPI(Resource):

    _model = IntrusionTestWSIModel()

    @check_token()
    def get(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ','')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            _user_intrusion_test = IntrusionTestWSIModel.query.filter_by(email=_user.email).first()

            if _user_intrusion_test is None:
                response = build_response_header(access_token=_access_token, status_code=200, data=None, error_message=None)
            else:
                response = build_response_header(access_token=_access_token, status_code=200, data=_user_intrusion_test.result, error_message=None)

            return response

        except Exception as e:
            raise InternalServerError

