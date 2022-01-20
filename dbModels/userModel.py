from dbModels import db
from dbModels.intrusionTestModels import IntrusionTestTIModel, IntrusionTestWSIModel, IntrusionTestWIModel
from dbModels.sysRecAndMapQuestions import SysRecAndMapQuestionsModel
from dbModels.sysRecSemanticMapQuestionsModel import SysRecSemanticMapQuestionsModel
from dbModels.sysRecVideoListeningTestModels import VideoListeningTestModel
from dbModels.sysRecRecommendationModel import RecommendationModel
from dbModels.sysRecColdStartModel import SysRecColdStartModel
from dbModels.sysRecUserAreaInterest import SysRecUserAreaInterest
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin


class UserModel(UserMixin, db.Model):

    __tablename__ = 'users'

    email = db.Column(db.String(), primary_key=True, unique=True)
    access_token = db.Column(db.String())
    refresh_token = db.Column(db.String())
    is_admin = db.Column(db.Boolean)
    fic_acceptance = db.Column(db.Boolean, default=False)
    know_peppa_pig = db.Column(db.Boolean, default=False)

    # make a relationship with other tables
    ti_results = db.relationship(IntrusionTestTIModel, backref='users', lazy=True)
    wi_results = db.relationship(IntrusionTestWSIModel, backref='users', lazy=True)
    wsi_results = db.relationship(IntrusionTestWIModel, backref='users', lazy=True)

    sysrec_user_video_listening_results = db.relationship(VideoListeningTestModel, backref='users', lazy=True)
    sysrec_user_recommendation = db.relationship(RecommendationModel, backref='users', lazy=True)
    sysrec_user_cold_start = db.relationship(SysRecColdStartModel, backref='users', lazy=True)
    sysrec_user_interest_area = db.relationship(SysRecUserAreaInterest, backref='users', lazy=True)
    sysrec_user_open_question_semantic_map = db.relationship(SysRecSemanticMapQuestionsModel, backref='users', lazy=True)
    sysrec_user_and_map_questions = db.relationship(SysRecAndMapQuestionsModel, backref='users', lazy=True)


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
        self.know_peppa_pig = False

        if email == 'simonolivierharel@gmail.com':
            self.is_admin = True

        self.save_to_db()
        return self.is_admin, self.fic_acceptance, self.know_peppa_pig

    def update_access_token(self, access_token, email):
        try:
            user = UserModel.query.filter_by(email=email).first()
            user.access_token = access_token
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def save_fic_acceptance(self, acceptance, email):
        try:
            user_session = UserModel.query.filter_by(email=email).first()
            user_session.fic_acceptance = acceptance
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def save_know_peppa_pig(self, know_peppa_pig, email):
        try:
            user_session = UserModel.query.filter_by(email=email).first()
            user_session.know_peppa_pig = know_peppa_pig
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


