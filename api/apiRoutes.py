import config as config
from api.apiAdmin import AdminConsentAPI
from api.apiSemanticMap import SemanticMapAPI
from flask_restful import Api
from api.apiUser import UserAPI, UserLoginAPI, UserLogoutAPI
from api.apiIntrusionTests import IntrusionTestWSIAPI, IntrusionTestWIAPI, IntrusionTestTIAPI, \
    ResultsIntrusionTestWIAPI, ResultsIntrusionTestWSIAPI, ResultsIntrusionTestTIAPI
from api.apiVideoListeningTest import VideoListeningTestAPI
from api.apiRecommendations import RecommendationAPI
from api.apiColdStart import ColdStartAPI
from api.apiUserInterestArea import UserInterestAreaAPI
from api.apiConsentForm import ConsentFormAPI

api = Api(prefix=config.API_PREFIX)


# API Endpoints

# User
api.add_resource(UserLoginAPI, '/user/login')
api.add_resource(UserLogoutAPI, '/user/logout')

# Test instrusion
api.add_resource(IntrusionTestTIAPI, '/ti-intrusion-test')
api.add_resource(ResultsIntrusionTestTIAPI, '/ti-intrusion-test-results')
api.add_resource(IntrusionTestWIAPI, '/wi-intrusion-test')
api.add_resource(ResultsIntrusionTestWIAPI, '/wi-intrusion-test-results')
api.add_resource(IntrusionTestWSIAPI, '/wsi-intrusion-test')
api.add_resource(ResultsIntrusionTestWSIAPI, '/wsi-intrusion-test-results')

# FIC
#api.add_resource(ConsentFormAPI, '/consent-form') # n'est plus utilisee

# MAP
api.add_resource(SemanticMapAPI, '/semantic-map')

# Sys-Rec
api.add_resource(ColdStartAPI, '/cold-start-choices')
api.add_resource(RecommendationAPI, '/recommendations')
api.add_resource(UserInterestAreaAPI, '/user-interest-area')

# A refaire
api.add_resource(VideoListeningTestAPI, '/video-listening-test')

# Admin
api.add_resource(AdminConsentAPI,'/admin-consent-form')
