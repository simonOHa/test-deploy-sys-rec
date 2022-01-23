import config as config
from api.apiAdmin import AdminConsentAPI
from api.apiGlobalComment import GlobalCommentAPI
from api.apiIsTestsCompleted import isTestCompletedAPI
from api.apiKnowPeppaPigForm import KnowPeppaPigFormAPI
from api.apiPredilectionTerm import PredilectionTermAPI
from api.apiSemanticMapQuestions import SemanticMapQuestionsAPI, SemanticMapQuestionsResultsAPI
from api.apiSemanticMap import SemanticMapAPI
from flask_restful import Api

from api.apiSysRecAndMapQuestions import SysRecAndMapQuestionsAPI
from api.apiUser import UserLoginAPI
from api.apiIntrusionTests import IntrusionTestWSIAPI, IntrusionTestWIAPI, IntrusionTestTIAPI, \
    ResultsIntrusionTestWIAPI, ResultsIntrusionTestWSIAPI, ResultsIntrusionTestTIAPI
from api.apiVideoListeningTest import VideoListeningTestAPI, ResultsVideoListeningTestAPI
from api.apiRecommendations import RecommendationAPI, ResultsRecommendationAPI
from api.apiColdStart import ColdStartAPI, ResultColdStartAPI
from api.apiUserInterestArea import UserInterestAreaAPI
from api.apiConsentForm import ConsentFormAPI

api = Api(prefix=config.API_PREFIX)


# API Endpoints

# User, FIC and Know Peppa pig
api.add_resource(UserLoginAPI, '/user/login')
api.add_resource(ConsentFormAPI, '/consent-form')
api.add_resource(KnowPeppaPigFormAPI, '/know-peppa-pig')
api.add_resource(isTestCompletedAPI, '/save-completed-test')


# Test instrusion
api.add_resource(IntrusionTestTIAPI, '/ti-intrusion-test')
api.add_resource(ResultsIntrusionTestTIAPI, '/ti-intrusion-test-results')
api.add_resource(IntrusionTestWIAPI, '/wi-intrusion-test')
api.add_resource(ResultsIntrusionTestWIAPI, '/wi-intrusion-test-results')
api.add_resource(IntrusionTestWSIAPI, '/wsi-intrusion-test')
api.add_resource(ResultsIntrusionTestWSIAPI, '/wsi-intrusion-test-results')



# Sys-Rec
# - test #1
api.add_resource(VideoListeningTestAPI, '/video-listening-test')
api.add_resource(ResultsVideoListeningTestAPI, '/video-listening-test-results')

# - MAP, test #2
api.add_resource(SemanticMapAPI, '/semantic-map')
api.add_resource(SemanticMapQuestionsAPI, '/open-questions-semantic-map')
api.add_resource(SemanticMapQuestionsResultsAPI, '/open-questions-semantic-map-results')

# - test #3
api.add_resource(ColdStartAPI, '/cold-start-choices')
api.add_resource(ResultColdStartAPI, '/cold-start-choices-result')
api.add_resource(PredilectionTermAPI, '/predilection-term')
api.add_resource(RecommendationAPI, '/recommendations')
api.add_resource(ResultsRecommendationAPI, '/recommendations-results')
api.add_resource(UserInterestAreaAPI, '/user-interest-area')
api.add_resource(SysRecAndMapQuestionsAPI, '/rec-and-map-questions')

# Global-comment
api.add_resource(GlobalCommentAPI, '/comment')


# Admin
api.add_resource(AdminConsentAPI, '/admin-consent-form')
