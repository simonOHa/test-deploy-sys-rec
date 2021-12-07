from flask_restful import Resource
from flask import request
from api.token import check_token
from api.http_header import build_response_header_extract_user_email
from dbModels.sysRecOpenQuestionSemanticMapModel import SysRecOpenQuestionSemanticMapModel


class OpenQuestionSemanticMapAPI(Resource):

    _model = SysRecOpenQuestionSemanticMapModel()

    @check_token()
    def get(self):
        email = request.args.get('user_id')
        user = SysRecOpenQuestionSemanticMapModel.query.filter_by(email=email).first()
        if user is not None:
            results = {'question_1': user.question_1,
                       'question_2': user.question_2,
                       'question_3': user.question_3
                       }

            response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '),
                                                            data=results)
        else :
            response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '))

        return response

    def post(self):
        response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '))
        results = request.get_json()
        self._model.save_to_db(results=results['results'], email=email)
        return response
