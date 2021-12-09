from flask_restful import Resource
from flask import request
from dbModels.sysRecUserAreaInterest import SysRecUserAreaInterest
from api.token import check_token
from api.http_header import build_response_header_extract_user_email


class UserInterestAreaAPI(Resource):

    _model = SysRecUserAreaInterest()

    @check_token()
    def get(self):
        email = request.args.get('user_id')
        area_interest = self._model.get_user_area_interest(email=email)
        response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '), data=area_interest)
        return response





