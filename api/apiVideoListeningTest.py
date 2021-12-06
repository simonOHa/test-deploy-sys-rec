from flask_restful import Resource
from flask import request
from dbModels.sysRecTestModels import VideoListeningTestModel
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
        res = request.get_json()
        #return self._model.save_to_db(self._model, res), 200
        return 'POST from VideoListeningTestAPI', 200


