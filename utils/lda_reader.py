import pandas as pd
import os

# Singleton


class LDAReader:

    _instance = None

    _doc_topics_distribution_path = os.path.join(os.getcwd(), 'peppa-pig-data', 'lda-model', 'peppa-test-topic-terms-proba.csv')
    _videos_infos_path = os.path.join(os.getcwd(), 'peppa-pig-data', 'lda-model', 'with_pretreatment_span_7.csv')

    _doc_topics_distribution = None
    _videos_infos = None

    def __init__(self):
        self._doc_topics_distribution = pd.read_csv(self._doc_topics_distribution_path)
        self._doc_topics_distribution = self._doc_topics_distribution.rename(columns={'Unnamed: 0': "doc_id"})
        self._videos_infos = pd.read_csv(self._videos_infos_path)
        self._videos_infos = self._videos_infos.rename(columns={'Unnamed: 0': "doc_id"})

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)

        return cls._instance



    # def get_best_videos_for_topic(self, topic_id):
    #     topic_id = 't_'+ str(topic_id)
    #     docs = self._doc_topic.loc[(self._doc_topic[0] == topic_id)][0] # Colonne 0 fait reference aux proba les plus elevees
    #     docs_id = docs.index.values
    #     df = pd.DataFrame()
    #     for i in docs_id:
    #         df = df.append(self._videos_infos.iloc[int(i)], ignore_index=True)
    #
    #     df = df.rename(columns={'Unnamed: 0': "doc_id"})
    #     return df

    def get_doc_topic_distribution(self):
        return self._doc_topics_distribution

    def get_video_infos(self):
        return self._videos_infos
