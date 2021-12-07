from dbModels import db


class SysRecOpenQuestionSemanticMapModel(db.Model):

    __tablename__ = 'openQuestionSemanticMap'

    email = db.Column(db.String(), db.ForeignKey('users.email'), primary_key=True)
    question_1 = db.Column(db.String())
    question_2 = db.Column(db.String())
    question_3 = db.Column(db.String())

    def __init__(self):
        pass

    def save_to_db(self, results, email):
        user_session = SysRecOpenQuestionSemanticMapModel.query.filter_by(email=email).first()
        if user_session:
            self._update(user_session, results)
        else:
            self.email = email
            self.question_1 = results['question_1']
            self.question_2 = results['question_2']
            self.question_3 = results['question_3']
            self._save_to_db()

    def _update(self, session, results):
        session.question_1 = results['question_1']
        session.question_2 = results['question_2']
        session.question_3 = results['question_3']
        db.session.commit()

    def _save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

