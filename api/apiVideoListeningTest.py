from flask_restful import Resource, request
from dbModels.sysRecTestModels import VideoListeningTestModel


class VideoListeningTestAPI(Resource):

    _model = VideoListeningTestModel()

    def get(self):
        return self._model.get_videos_test1(), 200

    def post(self):
        res = request.get_json()
        #return self._model.save_to_db(self._model, res), 200
        return 'POST from VideoListeningTestAPI', 200


