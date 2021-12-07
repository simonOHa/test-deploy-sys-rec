from flask_restful import Resource
from flask import request
from dbModels.sysRecVideoListeningTestModels import VideoListeningTestModel
from api.token import check_token
from api.http_header import build_response_header_extract_user_email


class VideoListeningTestAPI(Resource):

    _model = VideoListeningTestModel()

    @check_token()
    def get(self):
        response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '),
                                                            data=self._model.get_videos_test1())
        return response

    @check_token()
    def post(self):
        response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '))
        results = request.get_json()
        self._model.save_to_db(results=results['results'], email=email)
        return response


class ResultsVideoListeningTestAPI(Resource):

    _model = VideoListeningTestModel()

    @check_token()
    def get(self):
        email = request.args.get('user_id')
        user = VideoListeningTestModel.query.filter_by(email=email).first()

        if user is None:
            response, email = build_response_header_extract_user_email(
                access_token=request.headers['Authorization'].strip('Bearer '))
        else:
            response, email = build_response_header_extract_user_email(
                access_token=request.headers['Authorization'].strip('Bearer '),
                data=user.results)

        return response




