from flask_restful import Resource
from flask import request
from api.token import check_token
from api.http_header import build_response_header
import pandas as pd
from dbModels.intrusionTestModels import IntrusionTestTIModel, IntrusionTestWIModel, IntrusionTestWSIModel
from dbModels.sysRecSemanticMapQuestionsModel import SysRecSemanticMapQuestionsModel
from dbModels.sysRecRecommendationModel import RecommendationModel
from dbModels.sysRecUserAreaInterest import SysRecUserAreaInterest
from dbModels.sysRecVideoListeningTestModels import VideoListeningTestModel
from dbModels.userModel import UserModel
from api.errors import InternalServerError


class AdminConsentAPI(Resource):

    @check_token()
    def get(self):

        try:
            _access_token = request.headers['Authorization'].replace('Bearer ','')
            _user = UserModel.query.filter_by(access_token=_access_token).first()

            if _user is not None and _user.is_admin:
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

                sys_rec_test1_all = VideoListeningTestModel.query.all()
                sys_rec_test1_all_res = []
                for user in sys_rec_test1_all:
                    sys_rec_test1_all_res.append({'email': user.email,
                                                   'results': user.results
                                                   })

                sys_rec_test2_all = SysRecSemanticMapQuestionsModel.query.all()
                sys_rec_test2_all_res = []
                for user in sys_rec_test2_all:
                    sys_rec_test2_all_res.append({'email': user.email,
                                                  'question_1': user.question_1,
                                                  'question_2': user.question_2,
                                                  'question_3': user.question_3
                                                  })

                sys_rec_test3_videos_all = RecommendationModel.query.all()
                sys_rec_test3_videos_res = []
                for user in sys_rec_test3_videos_all:
                    cold_start_rec = None
                    other_rec = []
                    for k, v in user.recommendations.items():
                        if k == 'cold_start_rec':
                            cold_start_rec = v
                        else:
                            for val in v:
                                if val['videoRating']:
                                    other_rec.append(val)

                    sys_rec_test3_videos_res.append({'email': user.email,
                                                     'cold_start': cold_start_rec,
                                                     'recommendations': other_rec,
                                                      'total_rec_send': user.total_rec_send
                                                  })

                sys_rec_test3_area_interest_all = SysRecUserAreaInterest.query.all()
                sys_rec_test3_area_interest_res = []
                for user in sys_rec_test3_area_interest_all:
                    cold_start_rec = None
                    other_rec = []
                    for k, v in user.area_interest.items():
                        if k == 'cold_start':
                            kk = []
                            vv = []
                            for obj in v:
                                for kkk, vvv in obj.items():
                                    kk.append(kkk)
                                    vv.append(vvv)

                            xxx_series = pd.Series(data=vv, index=kk)
                            res = xxx_series.sort_values(ascending=False)[0:1]
                            top = res.to_dict()
                            cold_start_rec = top
                        else:
                            kk = []
                            vv = []
                            for obj in v:
                                for kkk, vvv in obj.items():
                                    kk.append(kkk)
                                    vv.append(vvv)

                            xxx_series = pd.Series(data=vv, index=kk)
                            res = xxx_series.sort_values(ascending=False)[0:3]
                            top = res.to_dict()
                            other_rec.append({'id': k, 'coordinates': top})

                    sys_rec_test3_area_interest_res.append({'email': user.email,
                                                            'cold_start': cold_start_rec,
                                                            'recommendations': other_rec
                                                  })


                grouped = {
                    'consent_form':consent_form_all_res,
                    'intrusion_TI_test': intrusion_TI_test_all_res,
                    'intrusion_WI_test': intrusion_WI_test_all_res,
                    'intrusion_WSI_test': intrusion_WSI_test_all_res,
                    'sys_rec_test1': sys_rec_test1_all_res,
                    'sys_rec_test2': sys_rec_test2_all_res,
                    'sys_rec_test3_videos': sys_rec_test3_videos_res,
                    'sys_rec_test3_area_interest': sys_rec_test3_area_interest_res
                }
                response = build_response_header(access_token=_access_token, status_code=200, data=grouped, error_message=None)
            else:
                response = build_response_header(access_token=_access_token, status_code=401, data=None, error_message=None)

            return response

        except Exception as e:
            raise InternalServerError




