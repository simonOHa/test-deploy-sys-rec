from flask_restful import Resource
from flask import request
from dbModels.sysRecUserAreaInterest import SysRecUserAreaInterest
from api.token import check_token
from api.http_header import build_response_header
from dbModels.userModel import UserModel
from api.errors import InternalServerError


class UserInterestAreaAPI(Resource):

    _model = SysRecUserAreaInterest()

    @check_token()
    def get(self):
        try:
            _access_token = request.headers['Authorization'].replace('Bearer ', '')
            _user = UserModel.query.filter_by(access_token=_access_token).first()
            _area_interest = self._model.get_user_area_interest(email=_user.email)
            response = build_response_header(access_token=_access_token, status_code=200, data=_area_interest, error_message=None)

            return response
        except Exception as e:
            raise InternalServerError





