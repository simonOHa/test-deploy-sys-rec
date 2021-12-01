from dbModels import db
import pandas as pd
import os


class IntrusionTestTIModel(db.Model):

    __tablename__ = 'resultsIntrusionTestTI'

    email = db.Column(db.String(), db.ForeignKey('users.email'), primary_key=True)
    question = db.Column(db.ARRAY(db.Integer))
    result_candidate_id = db.Column(db.ARRAY(db.Integer))
    result_candidate_value = db.Column(db.ARRAY(db.String))

    _ti_file_path = os.path.join(os.getcwd(), 'intrusion_test_data', 'ti_test.csv')

    def __init__(self):
        pass

    def save_to_db(self, result, email):
        self.result_candidate_id = [int(k) for k in result['candidate_id']]
        self.result_candidate_value = result['candidate_value']
        self.question = [int(k) for k in result['question']]
        self.email = email

        # Validation si l'utilisateur modifie sa selection
        user_session = IntrusionTestTIModel.query.filter_by(email=email).first()
        if user_session:
            self.update(user_session)
        else:
            self._save_to_db()

    def update(self, session):
        session.result_candidate_id = self.result_candidate_id
        session.result_candidate_value = self.result_candidate_value
        session.question = self.question

        db.session.commit()

    def _save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

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


class IntrusionTestWIModel(db.Model):

    __tablename__ = 'resultsIntrusionTestWI'

    email = db.Column(db.String(), db.ForeignKey('users.email'), primary_key=True)
    question = db.Column(db.ARRAY(db.Integer))
    result = db.Column(db.ARRAY(db.String))


    _wi_file_path = os.path.join(os.getcwd(), 'intrusion_test_data', 'wi_test.csv')

    def __init__(self):
        pass

    def save_to_db(self, response, email):
        self.question = [int(k) for k in response['results'].keys()]
        self.result = [v for v in response['results'].values()]
        self.email = email

        # Validation si l'utilisateur modifie sa selection
        user_session = IntrusionTestWIModel.query.filter_by(email=email).first()
        if user_session:
            self.update(user_session)
        else:
            self._save_to_db()

    def update(self, session):
        session.question = self.question
        session.result = self.result
        db.session.commit()

    def _save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def read_wi_data(self):
        df = pd.read_csv(self._wi_file_path)
        d = dict(tuple(df.groupby('question')))
        json_list = {}
        for index in range(1, len(d) + 1):
            question_id = d[index]['question'].to_list()[0]
            json_list[question_id] = {'question': question_id, 'candidates': d[index]['candidates'].to_list()}

        return json_list


class IntrusionTestWSIModel(db.Model):

    __tablename__ = 'resultsIntrusionTestWSI'

    email = db.Column(db.String(), db.ForeignKey('users.email'), primary_key=True)
    question = db.Column(db.ARRAY(db.Integer))
    result = db.Column(db.ARRAY(db.String))

    _wsi_file_path = os.path.join(os.getcwd(), 'intrusion_test_data', 'wsi_test.csv')

    def __init__(self):
        pass

    def save_to_db(self, response, email):
        self.question = [int(k) for k in response['results'].keys()]
        self.result = [v for v in response['results'].values()]
        self.email = email

        # Validation si l'utilisateur modifie sa selection
        user_session = IntrusionTestWSIModel.query.filter_by(email=email).first()
        if user_session:
            self.update(user_session)
        else:
            self._save_to_db()

    def update(self, session):
        session.question = self.question
        session.result = self.result
        db.session.commit()

    def _save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def read_wsi_data(self):
        df = pd.read_csv(self._wsi_file_path)
        d = dict(tuple(df.groupby('question')))

        json_list = {}

        for index in range(1, len(d) + 1):
            question_id = d[index]['question'].to_list()[0]
            json_list[question_id] = {'question': question_id, 'candidates': d[index]['candidates'].to_list()}

        return json_list

