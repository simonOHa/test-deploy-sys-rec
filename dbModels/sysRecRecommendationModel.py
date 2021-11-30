from dbModels import db
from dbModels.sysRecColdStartModel import SysRecColdStartModel
from dbModels.sysRecUserAreaInterest import SysRecUserAreaInterest
from utils.recommendations_generator import RecommendationsGenerator
from sqlalchemy_json import NestedMutableJson


class RecommendationModel(db.Model):

    __tablename__ = 'recommendation'

    email = db.Column(db.String(), db.ForeignKey('users.email'), primary_key=True)
    recommendations = db.Column(NestedMutableJson)
    total_rec_send = db.Column(db.Integer)

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
            rec = self._recommenderGenerator.get_cold_start_videos(user_cold_start_position=user.cold_start_position)
            # ajouter update history des recs et du centre d'interet
            # history des rec aura les do_id + rating a null
            video_rec_empty_rating = {'cold_start_rec': []}
            for index, row in rec.iterrows():
                video_rec_empty_rating['cold_start_rec'].append({'doc_id': row['doc_id'], 'videoRating': None})

            # centre d'interet sera le topic id selectionne
            SysRecUserAreaInterest().set_user_area_interest_to_cold_start_position(email=self.email, cold_start_position=user.cold_start_position)

            self.recommendations = video_rec_empty_rating
            self.save_to_db()

        else:
            user_area_interest = SysRecUserAreaInterest.query.filter_by(email=email).first()
            rec = self._recommenderGenerator.get_new_recommendations(
                user_area_of_interest=user_area_interest.area_interest[str(user_recommendation_model.total_rec_send)],
                history_videos_rating=user_recommendation_model.recommendations,
                option=1)
            # ajouter update history des recs et du centre d'interet:
            # history des rec aura les do_id + rating a null
            video_rec_empty_rating = {user_recommendation_model.total_rec_send: []}

            for index, row in rec.iterrows():
                video_rec_empty_rating[user_recommendation_model.total_rec_send].append({
                    'doc_id': row['doc_id'],
                    'videoRating': None
                })

            user_recommendation_model.recommendations.update(video_rec_empty_rating)
            user_recommendation_model.total_rec_send += 1
            db.session.commit()

            # centre d'interet se fera lors update lors du save

        return rec

    def save_watched_videos(self, email, videos_rated):
        user = RecommendationModel.query.filter_by(email=email).first()

        # Note : pour la mise a jour du centre d'interet, je travaille avec l<ensemble des notes donnees
        # par l'utilisateur et non simplement avec les dernieres notes donnees. !!

        # Save result cold-start
        if user.total_rec_send == 1:
            user.recommendations['cold_start_rec'] = videos_rated
            # Update le centre d'interet
            SysRecUserAreaInterest().update_user_area_interest(email=email,
                                                               #values=user.recommendations['cold_start_rec'],
                                                               recommended_videos=user.recommendations,
                                                               calcul_index=1)

        else:
            user.recommendations[user.total_rec_send] = videos_rated
            # Update le centre d'interet
            SysRecUserAreaInterest().update_user_area_interest(email=email,
                                                               # values=user.recommendations[user.total_rec_send],
                                                               recommended_videos=user.recommendations,
                                                               calcul_index=user.total_rec_send)

        db.session.commit()

    def update(self, session):
        for ele in self.recommendations:
            session.recommendations.append(ele)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


