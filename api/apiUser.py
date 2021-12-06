from flask_restful import Resource, request
from dbModels.userModel import UserModel
from flask import jsonify, make_response, abort
from oauth2client import client
import httplib2


CLIENT_SECRETS_FILE = "client_secret.json"
# N'est plus utilise pour le moment


class UserAPI(Resource):
    _model = UserModel()

    def __init__(self):
        pass

    def get(self):
        return {"id": self._model.generate_user_id()}, 200


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

            user = UserModel.query.filter_by(email=credentials.id_token['email']).first()

            if user is None:
                is_admin, fic_acceptance = self._model.create_user(email=credentials.id_token['email'],
                                        access_token=credentials.access_token,
                                        refresh_token=credentials.refresh_token)
                access_token = credentials.access_token
                email = credentials.id_token['email']
                fic_acceptance = fic_acceptance
            else:
                access_token = user.access_token
                email = user.email
                is_admin = user.is_admin
                fic_acceptance = user.fic_acceptance

            response = make_response({
                'access_token': 'Bearer ' + access_token,
                'email': email,
                'is_admin': is_admin,
                'fic_acceptance': fic_acceptance
            }, 200)
            response.headers["Content-Type"] = "application/json"
            response.headers["Authorization"] = 'Bearer ' + access_token

            return response
        except Exception as error:
            print(error)
            abort(403)

# Log user out
class UserLogoutAPI(Resource):
    _model = UserModel()

    def __init__(self):
        pass

    def post(self):
        try:
            msg = self._model.revoke_user_token()
            print(msg)
            return make_response(jsonify({
                'msg': msg
            }))
        except Exception as error:
            print(error)
            abort(403)


