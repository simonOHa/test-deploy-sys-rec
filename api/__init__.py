from api.apiUser import UserAPI
from api.apiRoutes import api


def build_api(app):
    api.init_app(app)

