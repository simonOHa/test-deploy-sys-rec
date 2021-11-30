from dbModels import db
from utils.recommendations_generator import RecommendationsGenerator


class SysRecColdStartModel(db.Model):

    __tablename__ = 'coldStart'

    email = db.Column(db.String(), db.ForeignKey('users.email'), primary_key=True)
    cold_start_position = db.Column(db.String())
    cold_start_choices = db.Column(db.ARRAY(db.String))

    _recommenderGenerator = RecommendationsGenerator()

    def __init__(self):
        self.cold_start_choices = self._recommenderGenerator.get_cold_start_choices()

    def get_cold_start_choices(self):
        return {'choices': self.cold_start_choices.tolist()}

    def save_cold_start_choice(self, cold_start_choice, email):
        self.cold_start_position = cold_start_choice
        self.email = email

        # Validation si l'utilisateur modifie sa selection
        user_session = SysRecColdStartModel.query.filter_by(email=email).first()
        if user_session:
            self.update(user_session)
        else:
            self.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update(self, session):
        session.cold_start_position = self.cold_start_position
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
