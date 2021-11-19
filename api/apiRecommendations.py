from flask_restful import Resource, request
from dbModels.sysRecRecommendationModel import RecommendationModel

# Permet d'obtenir les recommandations, autant en cold-start quant fonction des interet de l'utilisateur


class RecommendationAPI(Resource):

    _model = RecommendationModel()

    def get(self):
        user_id = request.args.get('user_id')
        res = self._model.get_new_recommendations(user_id=user_id)
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

        return return_val, 200

    def post(self):
        res = request.get_json()
        return self._model.save_watched_videos(user_id=res['user_id'], videos_rated=res['videos']), 200


