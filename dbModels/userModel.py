from dbModels import db
import uuid
from dbModels.intrusionTestModels import ResultsIntrusionTestTI, ResultsIntrusionTestWSI, ResultsIntrusionTestWI
from dbModels.sysRecTestModels import VideoListeningTestModel
from dbModels.sysRecRecommendationModel import RecommendationModel
from dbModels.sysRecColdStartModel import SysRecColdStartModel


from dbModels.sysRecUserAreaInterest import SysRecUserAreaInterest


class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.String(), primary_key=True)

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

    def generate_user_id(self):
        self.id = str(uuid.uuid4())
        self.save_to_db()
        return self.id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
