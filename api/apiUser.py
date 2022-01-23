from flask_restful import Resource
from flask import request
from dbModels.userModel import UserModel
from flask import make_response
from oauth2client import client
import httplib2
from api.errors import InternalServerError
CLIENT_SECRETS_FILE = "client_secret.json"


class UserLoginAPI(Resource):

    _model = UserModel()

    def __init__(self):
        pass

    def post(self):
        try:
            res = request.get_json()
            auth_code = res['code']
            credentials = client.credentials_from_clientsecrets_and_code(CLIENT_SECRETS_FILE, ['email'], auth_code)
            http_auth = credentials.authorize(httplib2.Http()) # adds in the appropriate headers and then delegates to the original

            user = self._model.query.filter_by(email=credentials.id_token['email']).first()

            if user is None:
                is_admin, fic_acceptance, know_peppa_pig, is_test_1_completed,is_test_2_completed,is_test_3_completed = self._model.create_user(email=credentials.id_token['email'],
                                                                                   access_token=credentials.access_token,
                                                                                   refresh_token=credentials.refresh_token)
                access_token = credentials.access_token
                email = credentials.id_token['email']
                fic_acceptance = fic_acceptance
                know_peppa_pig = know_peppa_pig
                is_test_1_completed = is_test_1_completed
                is_test_2_completed = is_test_2_completed
                is_test_3_completed = is_test_3_completed

            else:
                access_token = user.access_token
                email = user.email
                is_admin = user.is_admin
                fic_acceptance = user.fic_acceptance
                know_peppa_pig = user.know_peppa_pig
                is_test_1_completed = user.is_test_1_completed
                is_test_2_completed = user.is_test_2_completed
                is_test_3_completed = user.is_test_3_completed

            response = make_response({
                'access_token': 'Bearer ' + access_token,
                'email': email,
                'is_admin': is_admin,
                'fic_acceptance': fic_acceptance,
                'know_peppa_pig': know_peppa_pig,
                'is_test_1_completed': is_test_1_completed,
                'is_test_2_completed': is_test_2_completed,
                'is_test_3_completed': is_test_3_completed,

            }, 200)

            response.headers["Content-Type"] = "application/json"
            response.headers["Authorization"] = 'Bearer ' + access_token

            return response

        except Exception as e:
            raise InternalServerError


