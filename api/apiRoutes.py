import config as config
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
#api.add_resource(UserAPI, '/user')
api.add_resource(UserLoginAPI, '/user/login')
api.add_resource(UserLogoutAPI, '/user/logout')

#api.add_resource(UserInfoAPI, '/user/info')
#api.add_resource(UserRefreshAPI, '/user/refresh')

api.add_resource(IntrusionTestTIAPI, '/ti-intrusion-test')
api.add_resource(ResultsIntrusionTestTIAPI, '/ti-intrusion-test-results')

api.add_resource(IntrusionTestWIAPI, '/wi-intrusion-test')
api.add_resource(ResultsIntrusionTestWIAPI, '/wi-intrusion-test-results')

api.add_resource(IntrusionTestWSIAPI, '/wsi-intrusion-test')
api.add_resource(ResultsIntrusionTestWSIAPI, '/wsi-intrusion-test-results')

api.add_resource(ConsentFormAPI, '/consent-form')


api.add_resource(SemanticMapAPI, '/semantic-map')

# Sys-Rec
api.add_resource(ColdStartAPI, '/cold-start-choices')
api.add_resource(RecommendationAPI, '/recommendations')
api.add_resource(UserInterestAreaAPI, '/user-interest-area')

# A refaire
api.add_resource(VideoListeningTestAPI, '/video-listening-test')
