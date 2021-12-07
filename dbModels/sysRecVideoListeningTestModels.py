from dbModels import db
from utils.lda_reader import LDAReader
from sqlalchemy_json import NestedMutableJson


class VideoListeningTestModel(db.Model):

	__tablename__ = 'videoListeningTestModel'

	email = db.Column(db.String(), db.ForeignKey('users.email'), primary_key=True)
	results = db.Column(NestedMutableJson)

	_lda_reader = LDAReader()

	def __init__(self):
		pass

	def get_videos_test1(self, top=5, topic_id='t_1'):
		_doc_topics_distribution = self._lda_reader.get_doc_topic_distribution()
		_videos_infos = self._lda_reader.get_video_infos()

		top_n = _doc_topics_distribution.sort_values(by=[topic_id], ascending=False)[0:top]
		res = _videos_infos[_videos_infos['doc_id'].isin(top_n['doc_id'].to_numpy())]

		return_val = {}
		for index, row in res.iterrows():
			return_val[str(row['doc_id'])] = {
				"doc_id": row['doc_id'],
				"transcription": row['transcription'],
				"title": row['title'],
				"start_time": row['start_time'],
				"end_time": row['end_time'],
				"url": row['url'],
				"total_time": row['total_time'],
				"total_words": row['total_words']
			}

		return return_val

	def save_to_db(self, results, email):
		user_session = VideoListeningTestModel.query.filter_by(email=email).first()
		if user_session:
			self._update(user_session,results)
		else:
			self.email = email
			self._save_to_db(results)

	def _update(self,session, results):
		session.results = results
		db.session.commit()

	def _save_to_db(self, results):
		self.results = results
		db.session.add(self)
		db.session.commit()




