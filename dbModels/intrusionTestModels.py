from dbModels import db
import pandas as pd
import os
from sqlalchemy.exc import IntegrityError
from sqlalchemy_json import NestedMutableJson


class IntrusionTestTIModel(db.Model):

    __tablename__ = 'resultsIntrusionTestTI'

    email = db.Column(db.String(), db.ForeignKey('users.email'), primary_key=True)
    question = db.Column(db.ARRAY(db.Integer))
    result_candidate_id = db.Column(db.ARRAY(db.Integer))
    result_candidate_value = db.Column(db.ARRAY(db.String))
    video_watched_extra_info = db.Column(db.ARRAY(NestedMutableJson))
    score = db.Column(db.Float)

    _ti_file_path = os.path.join(os.getcwd(), 'intrusion_test_data', 'ti_test.csv')

    def __init__(self):
        pass

    def save_to_db(self, result, email):
        # Validation si l'utilisateur modifie sa selection
        user_session = IntrusionTestTIModel.query.filter_by(email=email).first()
        result['score'] = self._calculate_score(result_candidate_ids=[int(k) for k in result['candidate_id']])

        if user_session:
            self._update(user_session, result)
        else:
            self.result_candidate_id = [int(k) for k in result['candidate_id']]
            self.result_candidate_value = result['candidate_value']
            self.question = [int(k) for k in result['question']]
            self.video_watched_extra_info = result['extra_info']
            self.email = email
            self.score = result['score']
            self._save_to_db()

    def _update(self, session, result):
        try:
            session.result_candidate_id = [int(k) for k in result['candidate_id']]
            session.result_candidate_value = result['candidate_value']
            session.question = [int(k) for k in result['question']]
            session.video_watched_extra_info = result['extra_info']
            session.score = result['score']
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def _save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def read_ti_data(self):
        df = pd.read_csv(self._ti_file_path)
        d = dict(tuple(df.groupby('question')))
        json_list = {}

        for index in range(1, len(d) + 1):
            question_id = d[index]['question'].to_list()[0]
            text = d[index]['text'].to_list()[0]
            candidates = []
            for i in range(0, len(d[index]['candidate_id'])):
                candidate_id = d[index]['candidate_id'].to_list()[i]
                candidate_value = d[index]['candidate_value'].to_list()[i]
                candidates.append({'candidate_id': str(candidate_id), 'candidate_value': candidate_value})
            json_list[question_id] = {'question': question_id,'text': text, 'candidates': candidates}

        return json_list

    def _calculate_score(self, result_candidate_ids):
        df = pd.read_csv(self._ti_file_path)
        df = df[['question', 'intruder_id']].drop_duplicates(subset=None, keep='first', inplace=False)
        total_good_answer = 0
        for index, expected in enumerate(df['intruder_id'].to_list()):
            if result_candidate_ids[index] == expected:
                total_good_answer += 1

        return total_good_answer/len(df['intruder_id'].to_list())

class IntrusionTestWIModel(db.Model):

    __tablename__ = 'resultsIntrusionTestWI'

    email = db.Column(db.String(), db.ForeignKey('users.email'), primary_key=True)
    question = db.Column(db.ARRAY(db.Integer))
    result = db.Column(db.ARRAY(db.String))
    score = db.Column(db.Float)

    _wi_file_path = os.path.join(os.getcwd(), 'intrusion_test_data', 'wi_test.csv')

    def __init__(self):
        pass

    def save_to_db(self, result, email):
        # Validation si l'utilisateur modifie sa selection
        user_session = IntrusionTestWIModel.query.filter_by(email=email).first()
        result['score'] = self._calculate_score(candidates=[v for v in result['results'].values()])
        if user_session:
            self._update(user_session, result)
        else:
            self.question = [int(k) for k in result['results'].keys()]
            self.result = [v for v in result['results'].values()]
            self.score = result['score']
            self.email = email
            self._save_to_db()

    def _update(self, session, result):
        try:
            session.question = [int(k) for k in result['results'].keys()]
            session.result = [v for v in result['results'].values()]
            session.score = result['score']
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def _save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def read_wi_data(self):
        df = pd.read_csv(self._wi_file_path)
        d = dict(tuple(df.groupby('question')))
        json_list = {}
        for index in range(1, len(d) + 1):
            question_id = d[index]['question'].to_list()[0]
            json_list[question_id] = {'question': question_id, 'candidates': d[index]['candidates'].to_list()}

        return json_list

    def _calculate_score(self, candidates):
        df = pd.read_csv(self._wi_file_path)
        df = df[['question', 'intruder']].drop_duplicates(subset=None, keep='first', inplace=False)
        total_good_answer = 0
        for index, expected in enumerate(df['intruder'].to_list()):
            if candidates[index] == expected:
                total_good_answer += 1

        return total_good_answer/len(df['intruder'].to_list())


class IntrusionTestWSIModel(db.Model):

    __tablename__ = 'resultsIntrusionTestWSI'

    email = db.Column(db.String(), db.ForeignKey('users.email'), primary_key=True)
    question = db.Column(db.ARRAY(db.Integer))
    result = db.Column(db.ARRAY(db.String))
    score = db.Column(db.Float)

    _wsi_file_path = os.path.join(os.getcwd(), 'intrusion_test_data', 'wsi_test.csv')

    def __init__(self):
        pass

    def save_to_db(self, result, email):
        user_session = IntrusionTestWSIModel.query.filter_by(email=email).first()
        result['score'] = self._calculate_score(candidates=[v for v in result['results'].values()])

        if user_session:
            self._update(user_session, result)
        else:
            self.question = [int(k) for k in result['results'].keys()]
            self.result = [v for v in result['results'].values()]
            self.email = email
            self.score = result['score']
            self._save_to_db()

    def _update(self, session, result):
        try:
            session.question = [int(k) for k in result['results'].keys()]
            session.result = [v for v in result['results'].values()]
            session.score = result['score']
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def _save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def read_wsi_data(self):
        df = pd.read_csv(self._wsi_file_path)
        d = dict(tuple(df.groupby('question')))
        json_list = {}
        for index in range(1, len(d) + 1):
            question_id = d[index]['question'].to_list()[0]
            json_list[question_id] = {'question': question_id, 'candidates': d[index]['candidates'].to_list()}

        return json_list

    def _calculate_score(self, candidates):
        df = pd.read_csv(self._wsi_file_path)
        df = df[['question', 'intruder']].drop_duplicates(subset=None, keep='first', inplace=False)
        total_good_answer = 0
        for index, expected in enumerate(df['intruder'].to_list()):
            if candidates[index] == expected:
                total_good_answer += 1

        return total_good_answer/len(df['intruder'].to_list())