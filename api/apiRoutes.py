import config as config
from api.apiSemanticMap import SemanticMapAPI
from flask_restful import Api
from api.apiUser import UserAPI, UserLoginAPI, UserLogoutAPI
from api.apiIntrusionTests import ResultsIntrusionTestWSI, ResultsIntrusionTestWI, ResultsIntrusionTestTI
from api.apiVideoListeningTest import VideoListeningTestAPI
from api.apiRecommendations import RecommendationAPI
from api.apiColdStart import ColdStartAPI
from api.apiUserInterestArea import UserInterestAreaAPI

api = Api(prefix=config.API_PREFIX)


# API Endpoints
#api.add_resource(UserAPI, '/user')
api.add_resource(UserLoginAPI, '/user/login')
api.add_resource(UserLogoutAPI, '/user/logout')

#api.add_resource(UserInfoAPI, '/user/info')
#api.add_resource(UserRefreshAPI, '/user/refresh')




api.add_resource(ResultsIntrusionTestTI, '/ti-intrusion-test-results')
api.add_resource(ResultsIntrusionTestWI, '/wi-intrusion-test-results')
api.add_resource(ResultsIntrusionTestWSI, '/wsi-intrusion-test-results')
api.add_resource(SemanticMapAPI, '/semantic-map')

# Sys-Rec
api.add_resource(ColdStartAPI, '/cold-start-choices')
api.add_resource(RecommendationAPI, '/recommendations')
api.add_resource(UserInterestAreaAPI, '/user-interest-area')

# A refaire
api.add_resource(VideoListeningTestAPI, '/video-listening-test')
