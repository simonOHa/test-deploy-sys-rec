from flask_restful import Resource
from flask import request
from dbModels.sysRecVideoListeningTestModels import VideoListeningTestModel
from api.token import check_token
from api.http_header import build_response_header
from dbModels.userModel import UserModel
from api.errors import InternalServerError


class VideoListeningTestAPI(Resource):

    _model = VideoListeningTestModel()

    @check_token()
    def get(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ', '')
            _data = self._model.get_videos_test1()
            response = build_response_header(access_token=_access_token, status_code=200, data=_data, error_message=None)
            return response
        except Exception as e:
            raise InternalServerError

    @check_token()
    def post(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ', '')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            results = request.get_json()
            VideoListeningTestModel().save_to_db(results=results['results'], email=_user.email)
            response = build_response_header(access_token=_access_token, status_code=200, data=None, error_message=None)
            return response
        except Exception as e:
            raise InternalServerError


class ResultsVideoListeningTestAPI(Resource):

    _model = VideoListeningTestModel()

    @check_token()
    def get(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ', '')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            user_video_listening_results = VideoListeningTestModel.query.filter_by(email=_user.email).first()

            if user_video_listening_results is None:
                response = build_response_header(access_token=_access_token, status_code=200, data=None, error_message=None)
            else:
                response = build_response_header(access_token=_access_token, status_code=200, data=user_video_listening_results.results, error_message=None)

            return response

        except Exception as e:
            raise InternalServerError




