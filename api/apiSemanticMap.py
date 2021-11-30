import os
from flask_restful import Resource, request
import json
from api.token import check_token
from api.http_header import buid_response_header_get


class SemanticMapAPI(Resource):
    _semantic_map_path = os.path.join(os.getcwd(), 'peppa-pig-data', 'semantic-map', 'grouped-peppa-pig-topic-words.json')

    @check_token()
    def get(self):
        response = buid_response_header_get(access_token=request.headers['Authorization'].strip('Bearer '),
                                            data=json.load(open(self._semantic_map_path)))
        return response
