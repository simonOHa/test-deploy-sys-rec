from flask_restful import Resource, request
from api.token import check_token
from api.http_header import build_response_header_extract_user_email
from dbModels.consentFormModel import ConsentFormModel
from dbModels.intrusionTestModels import IntrusionTestTIModel, IntrusionTestWIModel, IntrusionTestWSIModel
from dbModels.userModel import UserModel


class AdminConsentAPI(Resource):

    @check_token()
    def get(self):

        consent_form_all = UserModel.query.all()
        consent_form_all_res = []
        for user in consent_form_all:
            consent_form_all_res.append({'email': user.email, 'acceptance': user.fic_acceptance})

        intrusion_TI_test_all = IntrusionTestTIModel.query.all()
        intrusion_TI_test_all_res = []
        for user in intrusion_TI_test_all:
            intrusion_TI_test_all_res.append({'email': user.email,
                                               'question': user.question,
                                               'result_candidate_id': user.result_candidate_id,
                                               'result_candidate_value': user.result_candidate_value})

        intrusion_WI_test_all = IntrusionTestWIModel.query.all()
        intrusion_WI_test_all_res = []
        for user in intrusion_WI_test_all:
            intrusion_WI_test_all_res.append({'email': user.email,
                                           'question': user.question,
                                           'result': user.result})

        intrusion_WSI_test_all = IntrusionTestWSIModel.query.all()
        intrusion_WSI_test_all_res = []
        for user in intrusion_WSI_test_all:
            intrusion_WSI_test_all_res.append({'email': user.email,
                                           'question': user.question,
                                           'result': user.result})

        grouped = {
            'consent_form':consent_form_all_res,
            'intrusion_TI_test': intrusion_TI_test_all_res,
            'intrusion_WI_test': intrusion_WI_test_all_res,
            'intrusion_WSI_test': intrusion_WSI_test_all_res
        }

        response, email = build_response_header_extract_user_email(access_token=request.headers['Authorization'].strip('Bearer '),
                                                            data=grouped)

        return response

