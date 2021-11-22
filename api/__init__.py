from flask_cors import CORS
from api.apiUser import UserAPI
from api.apiRoutes import api


def build_api(app):
    CORS(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    api.init_app(app)

