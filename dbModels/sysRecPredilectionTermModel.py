from dbModels import db
from utils.recommendations_generator import RecommendationsGenerator
from sqlalchemy.exc import IntegrityError
from sqlalchemy_json import NestedMutableJson


class SysRecPredilectionTermModel(db.Model):

    __tablename__ = 'predilectionTerm'

    email = db.Column(db.String(), db.ForeignKey('users.email'), primary_key=True)
    predilection_term = db.Column(db.ARRAY(NestedMutableJson))

    _recommenderGenerator = RecommendationsGenerator()

    def __init__(self):
        pass

    def save_predilection_term(self, predilection_term, email):
        user_session = SysRecPredilectionTermModel.query.filter_by(email=email).first()
        if user_session:
            self._update(user_session, predilection_term)
        else:
            self.predilection_term = predilection_term
            self.email = email
            self.save_to_db()

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def _update(self, session, predilection_term):
        try:
            session.predilection_term = predilection_term
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

