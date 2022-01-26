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
    #question_1 = db.Column(NestedMutableJson)
    question_2 = db.Column(NestedMutableJson)
    question_3 = db.Column(NestedMutableJson)
    question_4 = db.Column(NestedMutableJson)
    #question_5 = db.Column(NestedMutableJson)

    _lda_reader = LDAReader()
    _questions = None

    def __init__(self):
        pass

    def get_questions(self, email):
        # Check for user response exist
        _user = SysRecAndMapQuestionsModel.query.filter_by(email=email).first()
        if _user is not None:
            self._questions = {
                #'question_1': _user.question_1,
                'question_2': _user.question_2,
                'question_3': _user.question_3,
                'question_4': _user.question_4,
                #'question_5': _user.question_5
            }
        else:
            self._build_questions(email=email)

        return self._questions

    def _build_questions(self, email):
        # Question 1

        # Extraire les top words de chaque video, like et dislike de toutes les recommandations
        topic_ids = self._extract_topic_ids_from_user_area_interest_v2(email=email)
        final_top_words = self._calculate_words_intersection_from_user_area_interest_v2(all_top_words=topic_ids)
        final_top_words = [{'term': word, 'checked': False} for word in final_top_words]

        user_cold_start = SysRecColdStartModel.query.filter_by(email=email).first()
        cold_start_top_n_words = self._lda_reader.get_top10_topic_terms(topic_id=user_cold_start.cold_start_position['topic'])

        question_1 = {'question': "Parmis la liste des termes si-dessous, cochez votre terme de prédilection s'il est présent \n",
                      'cold_start_top_words': cold_start_top_n_words,
                      'final_top_words': final_top_words,
                      'word_not_found': [],
                      'topic_ids': topic_ids,
                      'comments': ''
                      }

        # Question 2
        # 'question': "La carte sémantique m'a aidé à comprendre comment les recommandations étaient générées ?",
        question_2 = {'question': "En vous attardant sur la section de la carte que vous venez de mettre en évidence, est-ce que cette visualisation vous aide à comprendre comment les recommandations ont été générées ?",
                      'comments': "",
                      'slider': ""
                      }

        # Question 3
        # 'question': "J'ai trouvé utile l'évolution des centres d'intérêts (boules jaunes) ?"
        question_3 = {'question': ": Est-ce que l’évolution des centres d’intérêt vous parait logique ?",
                      'comments': "",
                      'slider': ""
                      }

        # Question 4
        # 'question': "En général, les recommandations correspondaient bien à ma thématique de départ ?",
        question_4 = {'question': "En général, les recommandations correspondaient bien à ma thématique de départ ?",
                      'comments': "",
                      'slider': ""
                      }

        # Question 5
        question_5 = {'question': "À la fin de la session, j'étais satisfait des recommandations ?",
                      'comments': "",
                      'slider': ""
                      }

        self._questions = {
            # 'question_1': question_1,
            'question_2': question_2,
            'question_3': question_3,
            'question_4': question_4,
            #'question_5': question_5
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

    def _extract_topic_ids_from_user_area_interest_v2(self, email, top_n=N_TOPIC_BUILDING_USER_INTEREST_AREA):
        user = RecommendationModel.query.filter_by(email=email).first()
        doc_topic_distribution = self._lda_reader.get_doc_topic_distribution()
        results = None
        if user is not None:
            results = {'like': {'topic_ids': []}, 'dislike': {'topic_ids': []}}
            topic_ids_like = []
            topic_ids_dislike = []
            for rec in user.recommendations.keys():
                for video in user.recommendations[rec]:
                    v = doc_topic_distribution[doc_topic_distribution['doc_id'] == video['doc_id']]
                    v.drop('doc_id', axis=1)
                    v = v.drop('doc_id', axis=1)
                    topic_id = v.idxmax(1)
                    if video['videoRating'] == 'aime':
                        topic_ids_like.append(topic_id.item())
                    else:
                        topic_ids_dislike.append(topic_id.item())

            topic_ids_like = list(set(topic_ids_like))
            results['like']['topic_ids'] = topic_ids_like
            topic_ids_dislike = list(set(topic_ids_dislike))
            results['dislike']['topic_ids'] = topic_ids_like

            #for id in topic_ids_like:
            #    results['like']['words'].append(self._lda_reader.get_top10_topic_terms(topic_id=id))

            #for id in topic_ids_dislike:
            #    results['dislike']['words'].append(self._lda_reader.get_top10_topic_terms(topic_id=id))

        else:
            print('ERRRROOOORR from SysRecAndMapQuestionsModel')

        return results

    def _convert_to_front_end_object(self, datas):
        final_obj = []
        for data in datas:
            final_obj.append({'term': data, 'checked': False})

    def _calculate_words_intersection_from_user_area_interest_v2(self, all_top_words, n_most_commun = 10):
        # Cas a regarder :
        #   Si les topic_ids de like = dislike => On garde les mots de like
        #   Si les topic_ids de like != dislike => Soustraire les mots de dislike de l<ensemble de mots
        if all_top_words['like']['topic_ids'] == all_top_words['dislike']['topic_ids']:
            like_words = [self._lda_reader.get_top10_topic_terms(topic_id=id) for id in all_top_words['like']['topic_ids']]
            flat_list = [item for sublist in like_words for item in sublist]
            final_terms = [val[0] for val in Counter(flat_list).most_common(n_most_commun)]
        else:
            # Check si topic_id en commun entre les 2 listes
            _intersect = list(set(all_top_words['like']['topic_ids']) & set(all_top_words['dislike']['topic_ids']))
            if _intersect:
                # Delete topic_id en commun dans dislike
                for id in _intersect:
                    all_top_words['dislike']['topic_ids'].remove(id)

            # Recuperer les termes pour des differents topics
            dislike_words = [self._lda_reader.get_top10_topic_terms(topic_id=id) for id in all_top_words['dislike']['topic_ids']]
            like_words = [self._lda_reader.get_top10_topic_terms(topic_id=id) for id in all_top_words['like']['topic_ids']]

            dislike_words_flat_list = [item for sublist in dislike_words for item in sublist]
            like_words_flat_list = [item for sublist in like_words for item in sublist]

            # Intersection
            _words_intersect = list(set(like_words_flat_list) & set(dislike_words_flat_list))

            # Elimier les termes de l'intersection a like des likes
            for id in _words_intersect:
                like_words_flat_list.remove(id)

            final_terms = [val[0] for val in Counter(like_words_flat_list).most_common(n_most_commun)]

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
            # self.question_1 = results['question_1']
            self.question_2 = results['question_2']
            self.question_3 = results['question_3']
            self.question_4 = results['question_4']
            # self.question_5 = results['question_5']
            self._save_to_db()

    def _update(self, session, results):
        try:
            # session.question_1 = results['question_1']
            session.question_2 = results['question_2']
            session.question_3 = results['question_3']
            session.question_4 = results['question_4']
            # session.question_5 = results['question_5']
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def _save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
