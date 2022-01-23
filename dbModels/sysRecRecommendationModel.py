from dbModels import db
from dbModels.sysRecColdStartModel import SysRecColdStartModel
from dbModels.sysRecUserAreaInterest import SysRecUserAreaInterest
from utils.recommendations_generator import RecommendationsGenerator
from sqlalchemy_json import NestedMutableJson
from sqlalchemy.exc import IntegrityError
from config.CONSTANTS import *


class RecommendationModel(db.Model):

    __tablename__ = 'recommendation'

    email = db.Column(db.String(), db.ForeignKey('users.email'), primary_key=True)
    recommendations = db.Column(NestedMutableJson)
    total_rec_send = db.Column(db.Integer) # Une recommandation peut contenir plus d'une video
    distance = db.Column(NestedMutableJson)
    total_videos_sent = db.Column(db.Integer)
    is_end_of_recommendations = db.Column(db.Boolean, default=False)

    _recommenderGenerator = RecommendationsGenerator()

    def __init__(self):
        pass

    def get_new_recommendations(self, email):

        user_recommendation_model = RecommendationModel.query.filter_by(email=email).first()

        # Cold start recommendations
        if user_recommendation_model is None:
            self.email = email
            self.total_rec_send = 1
            user = SysRecColdStartModel.query.filter_by(email=email).first()
            rec = self._recommenderGenerator.get_cold_start_videos(user_cold_start_position=user.cold_start_position['topic'],
                                                                   top=TOP_N_VIDEOS_COLD_START)
            # ajouter update history des recs et du centre d'interet
            # history des rec aura les do_id + rating a null
            video_rec_empty_rating = {'cold_start_rec': []}
            for index in range(0, len(rec['recommendations'])):
                video_rec_empty_rating['cold_start_rec'].append({'doc_id': rec['recommendations'][index]['doc_id'], 'videoRating': None})

            # centre d'interet sera le topic id selectionne
            SysRecUserAreaInterest().set_user_area_interest_to_cold_start_position(email=self.email, cold_start_position=user.cold_start_position['topic'])

            self.distance = {}
            self.total_videos_sent = TOP_N_VIDEOS_COLD_START
            self.recommendations = video_rec_empty_rating
            self.save_to_db()

        else:
            if (user_recommendation_model.total_videos_sent < MAX_VIDEOS_CAN_BE_WATCH) & (user_recommendation_model.is_end_of_recommendations is False):

                user_area_interest = SysRecUserAreaInterest.query.filter_by(email=email).first()
                rec, distances = self._recommenderGenerator.get_new_recommendations(
                                                    user_area_of_interest=user_area_interest.area_interest[str(user_recommendation_model.total_rec_send)],
                                                    history_videos_rating=user_recommendation_model.recommendations,
                                                    option=NEW_REC_OPTION,
                                                    top=TOP_N_VIDEOS)

                # Ajouter update history des recs et du centre d'interet:
                # history des rec aura les do_id + rating a null
                video_rec_empty_rating = {user_recommendation_model.total_rec_send: []}
                _distance = {user_recommendation_model.total_rec_send: []}
                for index in range(0, len(rec['recommendations'])):
                    video_rec_empty_rating[user_recommendation_model.total_rec_send].append({
                        'doc_id': rec['recommendations'][index]['doc_id'],
                        'videoRating': None,
                        'distance': distances[index]
                    })

                    _distance[user_recommendation_model.total_rec_send].append({'doc_id': rec['recommendations'][index]['doc_id'],
                                                                                  'distance': distances[index]
                                                                                  })

                user_recommendation_model.distance.update(_distance)
                user_recommendation_model.is_end_of_recommendations = rec['recommendation_ended']
                user_recommendation_model.total_videos_sent += len(rec['recommendations'])
                user_recommendation_model.recommendations.update(video_rec_empty_rating)
                user_recommendation_model.total_rec_send += 1
                db.session.commit()

                # centre d'interet se fera lors du save
            else:
                user_recommendation_model.is_end_of_recommendations = True
                db.session.commit()
                rec = {'message': 'Fin des recommandations ! '}

        return rec

    def save_watched_videos(self, email, videos_rated):
        user = RecommendationModel.query.filter_by(email=email).first()

        # Note : pour la mise a jour du centre d'interet, j'utilise l'historique complet des videos regardees.

        # Save result cold-start
        if user.total_rec_send == 1:
            user.recommendations['cold_start_rec'] = videos_rated
            db.session.commit()
            SysRecUserAreaInterest().update_user_area_interest(email=email,
                                                               recommended_videos=user.recommendations,
                                                               calcul_index=1)

        else:
            # Afin de gerer le cas ou l'utilisateur envoie des modifications a ses anciennes recommandations.
            # Le front-end envoie une liste d'objets sans tenir compte de la structure en BD.
            # On sait que le nombre de videos pas envoie est de 5 (TOP_N_VIDEOS).
            if len(videos_rated) > TOP_N_VIDEOS:

                _user_rec = user.recommendations
                _total_videos_per_rec = []
                for k, v in user.recommendations.items():
                    _total_videos_per_rec.append(len(v))

                _start_at = 0
                for index, n_video in enumerate(_total_videos_per_rec):
                    if index == 0:
                        user.recommendations['cold_start_rec'] = videos_rated[_start_at:n_video]
                        # print(videos_rated[_start_at:n_video])
                        _start_at = n_video
                    else:
                        user.recommendations[index] = videos_rated[_start_at:_start_at + n_video]
                        # print(videos_rated[_start_at:_start_at + n_video])
                        _start_at = _start_at + n_video


                # Break a list into chunks of size TOP_N_VIDEOS
                # groups = [videos_rated[i:i + TOP_N_VIDEOS] for i in range(0, len(videos_rated), TOP_N_VIDEOS)]
                # if len(groups) != user.total_rec_send:
                #     print('Error in save_watched_videos')
                # for index, group in enumerate(groups):
                #     if index == 0:
                #         user.recommendations['cold_start_rec'] = group
                #     else:
                #         user.recommendations[index] = group

                db.session.commit()
                SysRecUserAreaInterest().update_user_area_interest(email=email,
                                                                   recommended_videos=user.recommendations,
                                                                   calcul_index=user.total_rec_send)

            else:
                user.recommendations[user.total_rec_send - 1] = videos_rated
                db.session.commit()
                # Update le centre d'interet
                SysRecUserAreaInterest().update_user_area_interest(email=email,
                                                                   recommended_videos=user.recommendations,
                                                                   calcul_index=user.total_rec_send)

    def update(self, session):
        try:
            for ele in self.recommendations:
                session.recommendations.append(ele)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
