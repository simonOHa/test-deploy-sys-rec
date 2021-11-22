from api.apiUser import UserAPI
from api.apiRoutes import api
from flask_cors import CORS

def build_api(app):

    api.init_app(app)
   
    CORS(api)

