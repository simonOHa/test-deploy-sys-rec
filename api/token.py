from functools import wraps
from flask import request, make_response, jsonify
import json
from dbModels.userModel import UserModel
from oauth2client import GOOGLE_REVOKE_URI, GOOGLE_TOKEN_URI, client
import httplib2

CLIENT_SECRETS_FILE = "client_secret.json"
client_secret = json.load(open(CLIENT_SECRETS_FILE))


def check_token():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            access_token = request.headers['Authorization'].strip('Bearer ')
            CLIENT_ID = client_secret['web']["client_id"]
            CLIENT_SECRET = client_secret['web']["client_secret"]

            user = UserModel.query.filter_by(access_token=access_token).first()

            if user is not None:
                credentials = client.OAuth2Credentials(
                    access_token=access_token,
                    client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET,
                    refresh_token=None,
                    token_expiry=None,
                    token_uri=GOOGLE_TOKEN_URI,
                    user_agent=None,
                    revoke_uri=GOOGLE_REVOKE_URI)

                if credentials.access_token_expired:
                    credentials = client.OAuth2Credentials(
                        access_token=None,  # set access_token to None since we use a refresh token
                        client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        refresh_token=user.refresh_token,
                        token_expiry=None,
                        token_uri=GOOGLE_TOKEN_URI,
                        user_agent=None,
                        revoke_uri=GOOGLE_REVOKE_URI)

                    credentials.refresh(httplib2.Http())  # refresh the access token (optional)
                    http = credentials.authorize(httplib2.Http())  # apply the credentials
                    user.update_access_token(credentials.access_token)
                    access_token = credentials.access_token

                return fn(*args, **kwargs)
            else:
                return jsonify(msg="BAD TOKEN"), 403

        return decorator
    return wrapper



def build_header():
    def wrapper(fn):
        @wraps(fn)
        def decorator():
            access_token = request.headers['Authorization'].strip('Bearer ')
            CLIENT_ID = client_secret['web']["client_id"]
            CLIENT_SECRET = client_secret['web']["client_secret"]

            return fn(access_token)

        return decorator
    return wrapper
