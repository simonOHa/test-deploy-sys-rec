from dbModels import db
from sqlalchemy.exc import IntegrityError
import pandas as pd
from collections import Counter
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
        top_words_per_topics = self._extract_top_words_from_user_area_interest(email=email)

        cold_start_id = top_words_per_topics['cold_start'][0]
        cold_start_top_n_words = self._lda_reader.get_top10_topic_terms(topic_id=cold_start_id)

        question_1 = {'question': "Est-ce que ?",
                      'cold_start_top_words': cold_start_top_n_words,
                      'final_top_words': self._calculate_words_intersection_from_user_area_interest(
                          runs_topic_ids=top_words_per_topics),
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
                topic_dist_list = user.area_interest[rec]
                k = []
                v = []
                for obj in topic_dist_list:
                    for kk, vv in obj.items():
                        k.append(kk)
                        v.append(vv)

                xxx_series = pd.Series(data=v, index=k)
                res = xxx_series.sort_values(ascending=False)[0:top_n]
                top = res.keys().to_list() #res.to_dict()
                response[rec] = top
                #response.append({rec: top})
        else:
            print('ERRRROOOORR from SysRecAndMapQuestionsModel')

        return response

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
