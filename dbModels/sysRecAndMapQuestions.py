from dbModels import db
from sqlalchemy.exc import IntegrityError
import pandas as pd
from collections import Counter

from dbModels.sysRecColdStartModel import SysRecColdStartModel
from dbModels.sysRecRecommendationModel import RecommendationModel
from dbModels.sysRecUserAreaInterest import SysRecUserAreaInterest
from utils.lda_reader import LDAReader
from config.CONSTANTS import *
from sqlalchemy_json import NestedMutableJson


class SysRecAndMapQuestionsModel(db.Model):
    __tablename__ = 'SysRecAndMapQuestions'

    email = db.Column(db.String(), db.ForeignKey('users.email'), primary_key=True)
    question_1 = db.Column(NestedMutableJson)
    question_2 = db.Column(NestedMutableJson)

    _lda_reader = LDAReader()
    _questions = None

    def __init__(self):
        pass

    def get_questions(self, email):

        # Check for user response exist
        _user = SysRecAndMapQuestionsModel.query.filter_by(email=email).first()
        if _user is not None:
            self._questions = {
                'question_1': _user.question_1,
                'question_2': _user.question_2
            }
        else:
            self._build_questions(email=email)

        return self._questions

    def _build_questions(self, email):
        # Question 1
        top_words_per_topics = self._extract_top_words_from_user_area_interest_v2(email=email) #self._extract_top_words_from_user_area_interest(email=email)
        user_cold_start = SysRecColdStartModel.query.filter_by(email=email).first()
        #cold_start_id = top_words_per_topics['cold_start'][0]
        cold_start_top_n_words = self._lda_reader.get_top10_topic_terms(topic_id=user_cold_start.cold_start_position)

        all_top_words = top_words_per_topics
        final_top_words = self._calculate_words_intersection_from_user_area_interest_v2(all_top_words=all_top_words)#self._calculate_words_intersection_from_user_area_interest(runs_topic_ids=top_words_per_topics)

        question_1 = {'question': "Est-ce que ?",
                      'cold_start_top_words': cold_start_top_n_words,
                      'final_top_words': final_top_words,
                      'answer': ''
                      }

        # Question 2
        question_2 = {'question': "Est-ce que les point jaunes ...?",
                      'answer': ''}

        self._questions = {
            'question_1': question_1,
            'question_2': question_2
        }

    def _extract_top_words_from_user_area_interest(self, email, top_n=N_TOPIC_BUILDING_USER_INTEREST_AREA):
        user = SysRecUserAreaInterest.query.filter_by(email=email).first()
        response = None
        if user is not None:
            response = {}
            for rec in user.area_interest.keys():
                # topic_dist_list = user.area_interest[rec]
                k = []
                v = []
                for obj in user.area_interest[rec]:
                    for kk, vv in obj.items():
                        k.append(kk)
                        v.append(vv)

                xxx_series = pd.Series(data=v, index=k)
                res = xxx_series.sort_values(ascending=False)[0:top_n]
                top = res.keys().to_list()
                response[rec] = top

        else:
            print('ERRRROOOORR from SysRecAndMapQuestionsModel')

        return response

    def _extract_top_words_from_user_area_interest_v2(self, email, top_n=N_TOPIC_BUILDING_USER_INTEREST_AREA):
        user = RecommendationModel.query.filter_by(email=email).first()
        doc_topic_distribution = self._lda_reader.get_doc_topic_distribution()
        topic_words = None
        if user is not None:
            topic_words = []
            for rec in user.recommendations.keys():
                for video in user.recommendations[rec]:
                    if video['videoRating'] == 'aime':
                        v = doc_topic_distribution[doc_topic_distribution['doc_id'] == video['doc_id']]
                        v.drop('doc_id', axis=1)
                        v = v.drop('doc_id', axis=1)
                        topic_id = v.idxmax(1)
                        print(topic_id)
                        top_words = self._lda_reader.get_top10_topic_terms(topic_id=topic_id.item())
                        topic_words.append(top_words)
        else:
            print('ERRRROOOORR from SysRecAndMapQuestionsModel')

        return topic_words

    def _calculate_words_intersection_from_user_area_interest_v2(self, all_top_words, n_most_commun = 10):
        flat_list = [item for sublist in all_top_words for item in sublist]
        final_terms = [val[0] for val in Counter(flat_list).most_common(n_most_commun)]
        print(Counter(flat_list))
        return final_terms

    def _calculate_words_intersection_from_user_area_interest(self, runs_topic_ids):
        list_terms = []
        for k, v in runs_topic_ids.items():
            if k == 'cold_start':
                list_terms.append(self._lda_reader.get_top10_topic_terms(topic_id=v[0]))
            else:
                for vv in v:
                    list_terms.append(self._lda_reader.get_top10_topic_terms(topic_id=vv))

        flat_list = [item for sublist in list_terms for item in sublist]
        final_terms = [val[0] for val in Counter(flat_list).most_common(10)]
        return final_terms

    def save_to_db(self, results, email):
        user_session = SysRecAndMapQuestionsModel.query.filter_by(email=email).first()
        if user_session:
            self._update(user_session, results)
        else:
            self.email = email
            self.question_1 = results['question_1']
            self.question_2 = results['question_2']
            self._save_to_db()

    def _update(self, session, results):
        try:
            session.question_1 = results['question_1']
            session.question_2 = results['question_2']
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def _save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
