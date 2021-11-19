from dbModels import db
import pandas as pd
import os


class ResultsIntrusionTestTI(db.Model):

    __tablename__ = 'resultsIntrusionTestTI'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.ARRAY(db.Integer))
    result_candidate_id = db.Column(db.ARRAY(db.Integer))
    result_candidate_value = db.Column(db.ARRAY(db.String))
    user_id = db.Column(db.String(), db.ForeignKey('users.id'))

    _ti_file_path = os.path.join(os.getcwd(), 'intrusion_test_data', 'ti_test.csv')

    def __init__(self):
        pass

    def save_to_db(self, model, result):
        model.result_candidate_id = result['candidate_id']
        model.result_candidate_value = result['candidate_value']
        model.question = result['question']
        model.user_id = result['id']
        db.session.add(model)
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


class ResultsIntrusionTestWI(db.Model):

    __tablename__ = 'resultsIntrusionTestWI'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.ARRAY(db.Integer))
    result = db.Column(db.ARRAY(db.String))
    user_id = db.Column(db.String(), db.ForeignKey('users.id'))

    _wi_file_path = os.path.join(os.getcwd(), 'intrusion_test_data', 'wi_test.csv')

    def __init__(self):
        pass

    def save_to_db(self, model, response):
        model.question = [int(k) for k in response['results'].keys()]
        model.result = [v for v in response['results'].values()]
        model.user_id = response['id']
        db.session.add(model)
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


class ResultsIntrusionTestWSI(db.Model):

    __tablename__ = 'resultsIntrusionTestWSI'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.ARRAY(db.Integer))
    result = db.Column(db.ARRAY(db.String))
    user_id = db.Column(db.String(), db.ForeignKey('users.id'))

    _wsi_file_path = os.path.join(os.getcwd(), 'intrusion_test_data', 'wsi_test.csv')
    def __init__(self):
        pass

    def save_to_db(self, model, response):
        model.question = [int(k) for k in response['results'].keys()]
        model.result = [v for v in response['results'].values()]
        model.user_id = response['id']
        db.session.add(model)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def read_wsi_data(self):
        df = pd.read_csv(self._wsi_file_path)
        d = dict(tuple(df.groupby('question')))

        json_list = {}

        for index in range(1, len(d) + 1):
            question_id = d[index]['question'].to_list()[0]
            json_list[question_id] = {'question': question_id, 'candidates': d[index]['candidates'].to_list()}

        return json_list

