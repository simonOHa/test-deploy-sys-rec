import os
from flask_restful import Resource
from flask import request
import json
from api.token import check_token
from api.http_header import build_response_header
from dbModels.userModel import UserModel
from api.errors import InternalServerError


class SemanticMapAPI(Resource):

    _semantic_map_path = os.path.join(os.getcwd(), 'peppa-pig-data', 'semantic-map', 'grouped-peppa-pig-topic-words.json')

    @check_token()
    def get(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ','')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            _data = json.load(open(self._semantic_map_path))
            response = build_response_header(access_token=_access_token, status_code=200, data=_data, error_message=None)

            return response

        except Exception as e:
            raise InternalServerError
