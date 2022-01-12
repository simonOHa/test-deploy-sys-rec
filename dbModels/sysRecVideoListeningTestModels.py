from dbModels import db
from utils.lda_reader import LDAReader
from sqlalchemy_json import NestedMutableJson
from sqlalchemy.exc import IntegrityError
from config.CONSTANTS import *


class VideoListeningTestModel(db.Model):

	__tablename__ = 'videoListeningTestModel'

	email = db.Column(db.String(), db.ForeignKey('users.email'), primary_key=True)
	results = db.Column(NestedMutableJson)

	_lda_reader = LDAReader()

	def __init__(self):
		pass

	def get_videos_test1(self, top=VIDEO_LISTENING_TOP_N_VIDEOS, topic_id=VIDEO_LISTENING_TOPIC_ID):
		_doc_topics_distribution = self._lda_reader.get_doc_topic_distribution()
		_videos_infos = self._lda_reader.get_video_infos()
		_top10_topic_terms = self._lda_reader.get_top10_topic_terms(topic_id=topic_id)

		top_n = _doc_topics_distribution.sort_values(by=[topic_id], ascending=False)[0:top]
		return_val = {'recommendations': [], 'top_terms': _top10_topic_terms}

		for id in top_n['doc_id']:
			info = _videos_infos[_videos_infos['doc_id'] == id]
			return_val['recommendations'].append({
												"doc_id": info['doc_id'].item(),
												"transcription": info['transcription'].item(),
												"title": info['title'].item(),
												"start_time_sec": info['start_time_sec'].item(),
												"end_time_sec": info['end_time_sec'].item(),
												"url": info['url'].item(),
												"youtube_video_id": info['youtube_video_id'].item()
												})
		return return_val

	def save_to_db(self, results, email):
		user_session = VideoListeningTestModel.query.filter_by(email=email).first()
		if user_session:
			self._update(user_session,results)
		else:
			self.email = email
			self._save_to_db(results)

	def _update(self, session, results):
		try:
			session.results = results
			db.session.commit()
		except IntegrityError:
			db.session.rollback()

	def _save_to_db(self, results):
		try:
			self.results = results
			db.session.add(self)
			db.session.commit()
		except IntegrityError:
			db.session.rollback()




