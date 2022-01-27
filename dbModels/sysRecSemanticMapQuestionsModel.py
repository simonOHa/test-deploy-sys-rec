from dbModels import db
from sqlalchemy.exc import IntegrityError
import random
from utils.lda_reader import LDAReader
from config.CONSTANTS import *


class SysRecSemanticMapQuestionsModel(db.Model):

    __tablename__ = 'SemanticMapQuestions'

    email = db.Column(db.String(), db.ForeignKey('users.email'), primary_key=True)
    question_1 = db.Column(db.Numeric())
    question_2 = db.Column(db.Numeric())
    question_3 = db.Column(db.ARRAY(db.String()))
    question_4 = db.Column(db.ARRAY(db.String()))

    _lda_reader = LDAReader()

    def __init__(self):
        pass

    def get_questions(self):
        topic_terms = self._lda_reader.get_topic_terms_distribution()
        n_words, n_topics = topic_terms.shape
        n_topics = n_topics

        # Build question 1
        total_choices = TOTAL_RANDOM_CHOICES
        random_choices = random.sample(range(int(n_topics / 2), n_topics + TOTAL_RANDOM_CHOICES_N_TOPIC_MAX),
                                       total_choices)
        if n_topics not in random_choices:
            random_choices[total_choices - 1] = n_topics

        question_1 = {'question': "Cette carte contient combien de thématique (boules rouges) ?",
                      'choices': random_choices,
                      'answer': n_topics
                      }

        # Build question 2
        total_choices = TOTAL_RANDOM_CHOICES

        random_choices = random.sample(range(5, n_words + TOTAL_RANDOM_CHOICES_N_WORDS_MAX), total_choices)
        if n_words not in random_choices:
            random_choices[total_choices - 1] = n_words

        question_2 = {'question': "Combien de termes sont associés à chaque thématique?",
                      'choices': random_choices,
                      'answer': n_words
                      }

        # Build question 3
        topic_id = QUESTION_3_TOPIC_ID
        question_3 = {'question': "Lister les termes associés à la thématique " + topic_id,
                      'answer': topic_terms['t_' + topic_id].to_list()
                      }

        # Build question 4
        topic_id_1 = QUESTION_4_TOPIC_1
        topic_id_2 = QUESTION_4_TOPIC_2
        terms_intersection = set(topic_terms['t_' + topic_id_1].to_list()).intersection(
            topic_terms['t_' + topic_id_2].to_list())

        question_4 = {
            'question': "Quel(s) est/sont le(s) terme(s) commun(s) aux ensembles " + topic_id_1 + " et " + topic_id_2,
            'answer': list(terms_intersection)
            }

        _questions = {
            'question_1': question_1,
            'question_2': question_2,
            'question_3': question_3,
            'question_4': question_4,
        }
        return _questions

    def save_to_db(self, results, email):
        user_session = SysRecSemanticMapQuestionsModel.query.filter_by(email=email).first()
        if user_session:
            self._update(user_session, results)
        else:
            print('SemanticMapQuestions')
            print(self.email)
            
            self.email = email
            self.question_1 = results['question_1']
            self.question_2 = results['question_2']
            self.question_3 = results['question_3']
            self.question_4 = results['question_4']
            self._save_to_db()

    def _update(self, session, results):
        try:
            session.question_1 = results['question_1']
            session.question_2 = results['question_2']
            session.question_3 = results['question_3']
            session.question_4 = results['question_4']
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def _save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


