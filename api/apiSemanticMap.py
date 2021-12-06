import os
from flask_restful import Resource
from flask import request
import json
from api.token import check_token
from api.http_header import build_response_header_extract_user_email


class SemanticMapAPI(Resource):
    _semantic_map_path = os.path.join(os.getcwd(), 'peppa-pig-data', 'semantic-map', 'grouped-peppa-pig-topic-words.json')

    @check_token()
    def get(self):
        response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '),
                                                            data=json.load(open(self._semantic_map_path)))
        return response
