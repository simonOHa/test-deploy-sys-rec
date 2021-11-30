from dbModels import db
from dbModels.intrusionTestModels import ResultsIntrusionTestTI, ResultsIntrusionTestWSI, ResultsIntrusionTestWI
from dbModels.sysRecTestModels import VideoListeningTestModel
from dbModels.sysRecRecommendationModel import RecommendationModel
from dbModels.sysRecColdStartModel import SysRecColdStartModel
from dbModels.sysRecUserAreaInterest import SysRecUserAreaInterest

from flask_login import UserMixin
from dbModels import login

class UserModel(UserMixin, db.Model):

    __tablename__ = 'users'

    email = db.Column(db.String(), primary_key=True, unique=True)
    access_token = db.Column(db.String())
    refresh_token = db.Column(db.String())

    # make a relationship with other tables
    ti_results = db.relationship(ResultsIntrusionTestTI, backref='users', lazy=True)
    wi_results = db.relationship(ResultsIntrusionTestWSI, backref='users', lazy=True)
    wsi_results = db.relationship(ResultsIntrusionTestWI, backref='users', lazy=True)

    sysrec_user_video_listening_results = db.relationship(VideoListeningTestModel, backref='users', lazy=True) # A refaire
    sysrec_user_recommendation = db.relationship(RecommendationModel, backref='users', lazy=True)
    sysrec_user_cold_start = db.relationship(SysRecColdStartModel, backref='users', lazy=True)
    sysrec_user_interest_area = db.relationship(SysRecUserAreaInterest, backref='users', lazy=True)

    def __init__(self):
        pass

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def create_user(self, email, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.email = email
        self.save_to_db()

    def update_access_token(self, access_token):
        self.access_token = access_token
        db.session.commit()

    # # A delete
    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)
    #
    # # A delete
    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)
    #
    # # On va avoir un probleme
    # def generate_user_id(self):
    #     #self.id = str(uuid.uuid4())
    #     self.save_to_db()
    #     return self.id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


