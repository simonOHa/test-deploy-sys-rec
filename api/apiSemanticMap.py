import os
from flask_restful import Resource, request
import json


class SemanticMapAPI(Resource):
    _semantic_map_path = os.path.join(os.getcwd(), 'peppa-pig-data', 'semantic-map', 'grouped-peppa-pig-topic-words.json')

    def get(self):
        return json.load(open(self._semantic_map_path)), 200