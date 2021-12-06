from flask_restful import Resource
from flask import request
from dbModels.sysRecRecommendationModel import RecommendationModel
from api.http_header import build_response_header_extract_user_email
from api.token import check_token


# Permet d'obtenir les recommandations, autant en cold-start quant fonction des interet de l'utilisateur


class RecommendationAPI(Resource):

    _model = RecommendationModel()

    @check_token()
    def get(self):
        email = request.args.get('user_id')
        res = self._model.get_new_recommendations(email=email)
        return_val = {}
        for index, row in res.iterrows():
            return_val[str(row['doc_id'])] = {
                "doc_id": row['doc_id'],
                "transcription": row['transcription'],
                "title": row['title'],
                "start_time": row['start_time'],
                "end_time": row['end_time'],
                "url": row['url'],
                "total_time": row['total_time'],
                "total_words": row['total_words']
            }
        response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '),
                                                                   data=return_val)
        return response

    @check_token()
    def post(self):
        response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '))
        res = request.get_json()
        self._model.save_watched_videos(email=email, videos_rated=res['videos'])
        return response




