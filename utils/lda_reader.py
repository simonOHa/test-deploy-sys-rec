import pandas as pd
import os

# Singleton


class LDAReader:

    _instance = None

    _doc_topics_distribution_path = os.path.join(os.getcwd(), 'peppa-pig-data', 'lda-model', 'doc-topic-distribution.csv')
    _videos_infos_path = os.path.join(os.getcwd(), 'peppa-pig-data', 'lda-model', 'video-info.csv')
    _top10_topic_terms_path = os.path.join(os.getcwd(), 'peppa-pig-data', 'lda-model', 'top10-topic-terms-distribution.csv')

    _doc_topics_distribution = None
    _videos_infos = None
    _top10_topic_terms = None

    def __init__(self):
        self._doc_topics_distribution = pd.read_csv(self._doc_topics_distribution_path)
        self._videos_infos = pd.read_csv(self._videos_infos_path)
        self._top10_topic_terms = pd.read_csv(self._top10_topic_terms_path)

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)

        return cls._instance

    def get_doc_topic_distribution(self):
        return self._doc_topics_distribution

    def get_video_infos(self):
        return self._videos_infos

    def get_top10_topic_terms(self, topic_id):
        return self._top10_topic_terms[topic_id].to_list()

    def get_topic_terms_distribution(self):
        return self._top10_topic_terms

    def get_all_topic_ids(self):
        return self._top10_topic_terms.columns.to_list()
