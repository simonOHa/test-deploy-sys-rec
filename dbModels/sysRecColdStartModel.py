from dbModels import db
from utils.recommendations_generator import RecommendationsGenerator
from sqlalchemy.exc import IntegrityError
from sqlalchemy_json import NestedMutableJson


class SysRecColdStartModel(db.Model):

    __tablename__ = 'coldStart'

    email = db.Column(db.String(), db.ForeignKey('users.email'), primary_key=True)
    cold_start_position = db.Column(NestedMutableJson)
    cold_start_choices = db.Column(db.ARRAY(NestedMutableJson))

    _recommenderGenerator = RecommendationsGenerator()

    def __init__(self):
        pass

    def get_cold_start_choices(self):
        self.cold_start_choices = self._recommenderGenerator.get_cold_start_choices()
        if len(self.cold_start_choices) > 0:
            return self.cold_start_choices
        else:
            return None

    def save_cold_start_choice(self, cold_start_choice, email):
        user_session = SysRecColdStartModel.query.filter_by(email=email).first()
        if user_session:
            self._update(user_session, cold_start_choice)
        else:
            self.cold_start_position = cold_start_choice
            self.email = email
            self.save_to_db()

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def _update(self, session, cold_start_choice):
        try:
            session.cold_start_position = cold_start_choice
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

