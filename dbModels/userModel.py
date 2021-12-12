from dbModels import db
from dbModels.intrusionTestModels import IntrusionTestTIModel, IntrusionTestWSIModel, IntrusionTestWIModel
from dbModels.sysRecVideoListeningTestModels import VideoListeningTestModel
from dbModels.sysRecRecommendationModel import RecommendationModel
from dbModels.sysRecColdStartModel import SysRecColdStartModel
from dbModels.sysRecUserAreaInterest import SysRecUserAreaInterest
from dbModels.consentFormModel import ConsentFormModel

from flask_login import UserMixin


class UserModel(UserMixin, db.Model):

    __tablename__ = 'users'

    email = db.Column(db.String(), primary_key=True, unique=True)
    access_token = db.Column(db.String())
    refresh_token = db.Column(db.String())
    is_admin = db.Column(db.Boolean)
    fic_acceptance = db.Column(db.Boolean)

    # make a relationship with other tables
    ti_results = db.relationship(IntrusionTestTIModel, backref='users', lazy=True)
    wi_results = db.relationship(IntrusionTestWSIModel, backref='users', lazy=True)
    wsi_results = db.relationship(IntrusionTestWIModel, backref='users', lazy=True)

    # Je pense qu'il en manque ...

    sysrec_user_video_listening_results = db.relationship(VideoListeningTestModel, backref='users', lazy=True) # A refaire
    sysrec_user_recommendation = db.relationship(RecommendationModel, backref='users', lazy=True)
    sysrec_user_cold_start = db.relationship(SysRecColdStartModel, backref='users', lazy=True)
    sysrec_user_interest_area = db.relationship(SysRecUserAreaInterest, backref='users', lazy=True)

    user_consent_form = db.relationship(ConsentFormModel, backref='users', lazy=True)

    def __init__(self):
        pass

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def create_user(self, email, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.email = email
        self.is_admin = False
        self.fic_acceptance = False

        if email == 'simonolivierharel@gmail.com':
            self.is_admin = True

        self.save_to_db()
        return self.is_admin, self.fic_acceptance

    def update_access_token(self, access_token, email):
        user = UserModel.query.filter_by(email=email).first()
        user.access_token = access_token
        db.session.commit()

    def save_fic_acceptance(self, acceptance, email):
        user = UserModel.query.filter_by(email=email).first()
        user.fic_acceptance = acceptance

        # if acceptance == 'true':
        #     user.fic_acceptance = True
        # else:
        #     user.fic_acceptance = False
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


