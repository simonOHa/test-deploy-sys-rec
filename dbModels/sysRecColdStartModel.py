from dbModels import db
from utils.recommendations_generator import RecommendationsGenerator


class SysRecColdStartModel(db.Model):

    __tablename__ = 'coldStart'

    user_id = db.Column(db.String(), db.ForeignKey('users.id'), primary_key=True)
    cold_start_position = db.Column(db.String())
    cold_start_choices = db.Column(db.ARRAY(db.String))

    _recommenderGenerator = RecommendationsGenerator()

    def __init__(self):
        self.cold_start_choices = self._recommenderGenerator.get_cold_start_choices()

    def get_cold_start_choices(self):
        return self.cold_start_choices

    def save_cold_start_choice(self, cold_start_choice, user_id):
        self.cold_start_position = cold_start_choice
        self.user_id = user_id

        # Validation si l'utilisateur modifie sa selection
        user_session = SysRecColdStartModel.query.filter_by(user_id=user_id).first()
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
