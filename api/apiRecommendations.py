from flask_restful import Resource
from flask import request
from dbModels.sysRecRecommendationModel import RecommendationModel
from api.http_header import build_response_header
from api.token import check_token
from utils.lda_reader import LDAReader
from dbModels.userModel import UserModel
from api.errors import InternalServerError
# Permet d'obtenir les recommandations, autant en cold-start quant fonction des interet de l'utilisateur


class RecommendationAPI(Resource):

    _model = RecommendationModel()

    @check_token()
    def get(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ', '')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            _new_recommendations = self._model.get_new_recommendations(email=_user.email)


            # _return_val = {}
            #
            # for index, row in _new_recommendations.iterrows():
            #     _return_val[str(row['doc_id'])] = {
            #         "doc_id": row['doc_id'],
            #         "transcription": row['transcription'],
            #         "title": row['title'],
            #         "start_time": row['start_time'],
            #         "end_time": row['end_time'],
            #         "url": row['url'],
            #         "total_time": row['total_time'],
            #         "total_words": row['total_words']
            #     }

            response = build_response_header(access_token=_access_token, status_code=200, data=_new_recommendations, error_message=None)
            return response

        except Exception as e:
            raise InternalServerError

    @check_token()
    def post(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ', '')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            _request = request.get_json()

            self._model.save_watched_videos(email=_user.email, videos_rated=_request['videos'])
            response = build_response_header(access_token=_access_token, status_code=200, data=None, error_message=None)

            return response

        except Exception as e:
            raise InternalServerError


class ResultsRecommendationAPI(Resource):

    _model = RecommendationModel()
    _lda_reader = LDAReader()
    _videos_infos = _lda_reader.get_video_infos()

    @check_token()
    def get(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ','')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            _user_recommendations_model = RecommendationModel.query.filter_by(email=_user.email).first()

            if _user_recommendations_model is not None:
                result = {'form': [], 'videos': []}
                for k, v in _user_recommendations_model.recommendations.items():
                    for vv in v:
                        result['form'].append(vv)
                        video_id = vv['doc_id']
                        video_info = self._videos_infos.iloc[video_id]
                        result['videos'].append({
                            "doc_id": int(video_info['doc_id']),
                            "transcription": video_info['transcription'],
                            "title": video_info['title'],
                            "start_time_sec": video_info['start_time_sec'],
                            "end_time_sec": video_info['end_time_sec'],
                            "url": video_info['url'],
                            "youtube_video_id": video_info['youtube_video_id']
                            })

                response = build_response_header(access_token=_access_token, status_code=200, data=result, error_message=None)
                return response
            else:
                response = build_response_header(access_token=_access_token, status_code=200, data=None,  error_message=None)
                return response
        except Exception as e:
            raise InternalServerError






