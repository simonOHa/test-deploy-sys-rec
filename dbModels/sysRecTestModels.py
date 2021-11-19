from dbModels import db
import os


class VideoListeningTestModel(db.Model):

    __tablename__ = 'videoListeningTestModel'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video = db.Column(db.ARRAY(db.Integer))
    rating = db.Column(db.ARRAY(db.Integer))
    comments = db.Column(db.ARRAY(db.String))
    user_id = db.Column(db.String(), db.ForeignKey('users.id'))

    _ti_file_path = os.path.join(os.getcwd(), 'intrusion_test_data', 'ti_test.csv')

    def __init__(self):
        pass


    def get_videos_test1(self):
        return {
	"0": {
		"doc_id": 0,
		"transcription": " little brother  daddy peppa george playing   house cat dream sure dinosaur grandpa planting seed",
		"title": "gardening",
		"start_time": "00:00:02.730",
		"end_time": "00:00:53.399",
		"url": "https:\\/\\/www.youtube.com\\/watch?v=CTZJSVbzdyU&feature=youtu.be&ab_channel=UCdRyB_BAJDfo0clpilGkFzQ",
		"total_time": 50.669,
		"total_words": 14
	},
	"264": {
		"doc_id": 264,
		"transcription": " little brother whoop  museum peppa family going museum patty museum place interesting thing old older yes older really old",
		"title": "the museum",
		"start_time": "00:00:02.700",
		"end_time": "00:00:42.989",
		"url": "https:\\/\\/www.youtube.com\\/watch?v=PpdIewQhnTo&feature=youtu.be&ab_channel=UCdRyB_BAJDfo0clpilGkFzQ",
		"total_time": 40.289,
		"total_words": 19
	},
	"272": {
		"doc_id": 272,
		"transcription": "cake  favorite room museum cafe come tuck yes nice room",
		"title": "the museum",
		"start_time": "00:04:28.199",
		"end_time": "00:04:40.050",
		"url": "https:\\/\\/www.youtube.com\\/watch?v=PpdIewQhnTo&feature=youtu.be&ab_channel=UCdRyB_BAJDfo0clpilGkFzQ",
		"total_time": 11.851,
		"total_words": 10
	},
	"273": {
		"doc_id": 273,
		"transcription": " little brother mommy pig study polly peppa family visiting   pig egg hello little one come inside surprise new pet guess",
		"title": "polly parrot",
		"start_time": "00:00:02.730",
		"end_time": "00:00:47.790",
		"url": "https:\\/\\/www.youtube.com\\/watch?v=KQbHc9abYMI&feature=youtu.be&ab_channel=UCdRyB_BAJDfo0clpilGkFzQ",
		"total_time": 45.06,
		"total_words": 20
	},
	"274": {
		"doc_id": 274,
		"transcription": "dinosaur dinosaur come   pet parrot peppa george pet parrot called polly pretty polly clever parrot mommy polly",
		"title": "polly parrot",
		"start_time": "00:00:50.460",
		"end_time": "00:01:27.570",
		"url": "https:\\/\\/www.youtube.com\\/watch?v=KQbHc9abYMI&feature=youtu.be&ab_channel=UCdRyB_BAJDfo0clpilGkFzQ",
		"total_time": 37.11,
		"total_words": 17
	}
}

    def save_to_db(self, model, result):
        model.result_candidate_id = result['candidate_id']
        model.result_candidate_value = result['candidate_value']
        model.question = result['question']
        model.user_id = result['id']
        db.session.add(model)
        db.session.commit()




