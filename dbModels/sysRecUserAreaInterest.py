from dbModels import db
from sqlalchemy_json import NestedMutableJson
from utils.recommendations_generator import RecommendationsGenerator
import pandas as pd
from sqlalchemy.exc import IntegrityError
from config.CONSTANTS import *


class SysRecUserAreaInterest(db.Model):

    __tablename__ = 'userAreaInterest'

    email = db.Column(db.String(), db.ForeignKey('users.email'), primary_key=True)
    area_interest = db.Column(NestedMutableJson)

    _recommenderGenerator = RecommendationsGenerator()

    def __init__(self):
        pass

    def get_user_area_interest(self, email, top_n=N_TOPIC_BUILDING_USER_INTEREST_AREA):
        user = SysRecUserAreaInterest.query.filter_by(email=email).first()
        response = None
        if user is not None:
            response = []
            for rec in user.area_interest.keys():
                topic_dist_list = user.area_interest[rec]
                k = []
                v = []
                for obj in topic_dist_list:
                    for kk, vv in obj.items():
                        k.append(kk)
                        v.append(vv)

                xxx_series = pd.Series(data=v, index=k)
                res = xxx_series.sort_values(ascending=False)[0:top_n]
                top = res.to_dict()
                response.append({'id': rec, 'coordinates': top})

        return response

    def set_user_area_interest_to_cold_start_position(self, email, cold_start_position):
        _cold_start_area_interest = self._recommenderGenerator.calculate_cold_start_user_area_interest(cold_start_position)
        user = SysRecUserAreaInterest.query.filter_by(email=email).first()
        if user is None:
            self.email = email
            self.area_interest = _cold_start_area_interest
            self.save_to_db()
        else:
            print('ERRRRRRRROOOOOOOOOORRRRRRRRRR')

    def update_user_area_interest(self, email, recommended_videos, calcul_index):
        new_area_of_interest = self._recommenderGenerator.calculate_center_of_interest(videos_rating=recommended_videos, option=1)
        user = SysRecUserAreaInterest.query.filter_by(email=email).first()
        result_to_save_in_db = {calcul_index: []}

        # Afin de gerer le cas ou aucun video a ete aime
        if new_area_of_interest is None:
            # Reprendre l'ancien centre dinteret
            result_to_save_in_db[calcul_index] = user.area_interest[list(user.area_interest.keys())[-1]]

        else:
            for colname, value in new_area_of_interest.items():
                result_to_save_in_db[calcul_index].append({
                    colname: value.values[0]
                })

        user.area_interest.update(result_to_save_in_db)
        db.session.commit()

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
