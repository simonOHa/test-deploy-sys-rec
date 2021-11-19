import pandas as pd
from utils.lda_reader import LDAReader


# Singleton


class RecommendationsGenerator:
    _instance = None

    _doc_topics_distribution = None
    _videos_infos = None
    _cold_start_choices = []  # list of topic ids ( ['t_1',...'t_K'])
    _lda_reader = LDAReader()

    def __init__(self):
        self._doc_topics_distribution = self._lda_reader.get_doc_topic_distribution()
        self._videos_infos = self._lda_reader.get_video_infos()
        self._cold_start_choices = self._build_cold_start_choices()

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)

        return cls._instance

    def calculate_cold_start_user_area_interest(self, cold_start_position):
        res = {'cold_start': []}
        for choice in self._cold_start_choices:
            probability = 0.0

            if choice == cold_start_position:
                probability = 1.0

            res['cold_start'].append({
                choice: probability
            })
        return res

    def calculate_center_of_interest(self, videos_rating, option=1):
        liked_videos = []
        disliked_videos = []
        for k, v in videos_rating.items():
            for video in v:
                if video['videoRating'] == 'aime':
                    liked_videos.append(video['doc_id'])
                else:
                    disliked_videos.append(video['doc_id'])

        # On considere seulement le videos : like
        if option == 1:
            if len(liked_videos) > 0:
                # Calcul
                liked_videos_topic_distribution = self._doc_topics_distribution[self._doc_topics_distribution['doc_id'].isin(liked_videos)]
                liked_videos_topic_distribution = liked_videos_topic_distribution[liked_videos_topic_distribution.columns.drop(['doc_id'])]
                liked_videos_topic_distribution_sum = liked_videos_topic_distribution.sum() / len(liked_videos)
                _user_area_of_interest = liked_videos_topic_distribution_sum / len(liked_videos)

                # Reshape result
                _user_area_of_interest = _user_area_of_interest.to_frame().transpose()
                return _user_area_of_interest

            # Si aucun videos n'a ete aime, on ne change pas le centre d'interet
            else:
                return None

        # On considere les videos : like et dislike
        elif option == 2:
            # Calcul
            if len(liked_videos) > 0 and len(disliked_videos) > 0:
                liked_videos_topic_distribution = self._doc_topics_distribution[self._doc_topics_distribution['doc_id'].isin(liked_videos)]
                liked_videos_topic_distribution = liked_videos_topic_distribution[liked_videos_topic_distribution.columns.drop(['doc_id'])]
                liked_videos_topic_distribution_sum = liked_videos_topic_distribution.sum()

                disliked_videos_topic_distribution = self._doc_topics_distribution[self._doc_topics_distribution['doc_id'].isin(disliked_videos)]
                disliked_videos_topic_distribution = disliked_videos_topic_distribution[disliked_videos_topic_distribution.columns.drop(['doc_id'])]
                disliked_videos_topic_distribution_sum = disliked_videos_topic_distribution.sum()

                diff = liked_videos_topic_distribution_sum - disliked_videos_topic_distribution_sum
                _user_area_of_interest = diff / (len(liked_videos) + len(disliked_videos))

                # Reshape result
                _user_area_of_interest = _user_area_of_interest.to_frame().transpose()
                return _user_area_of_interest

            elif len(liked_videos) > 0 and len(disliked_videos) == 0:
                liked_videos_topic_distribution = self._doc_topics_distribution[self._doc_topics_distribution['doc_id'].isin(liked_videos)]
                liked_videos_topic_distribution = liked_videos_topic_distribution[liked_videos_topic_distribution.columns.drop(['doc_id'])]
                liked_videos_topic_distribution_sum = liked_videos_topic_distribution.sum()

                _user_area_of_interest = liked_videos_topic_distribution_sum / len(liked_videos)

                # Reshape result
                _user_area_of_interest = _user_area_of_interest.to_frame().transpose()
                return _user_area_of_interest

            # Si aucun videos n'a ete aime, on ne change pas le centre d'interet
            elif len(liked_videos) == 0 and len(disliked_videos) > 0:
                return None

    def get_new_recommendations(self, user_area_of_interest, option=1, top=5, history_videos_rating=None):
        _doc_topics_distribution_interest = pd.DataFrame()

        # Extraction des probabilites du centre d'interet
        proba = []
        for val in user_area_of_interest:
            for k, v in val.items():
                proba.append(v)

        # Calcul des distances entre centre d'interet et tous les distribution doc-topic
        for index, row in self._doc_topics_distribution.iterrows():
            doc_id = row['doc_id']
            row = row.drop('doc_id')
            manhattan_distance = self._manhattan_distance(proba, row.to_list())
            df_tmp = pd.DataFrame([{'doc_id': doc_id, 'distance': manhattan_distance}])
            _doc_topics_distribution_interest = _doc_topics_distribution_interest.append(df_tmp, ignore_index=True)

        # On considere seulement le centre d'interet
        if option == 1:
            top_n = _doc_topics_distribution_interest.sort_values(by=['distance'], ascending=True)[0:top]

        # Serie d'options pour ne pas recommander des videos deja recommandees
        elif history_videos_rating:
            # On elimine tous le videos deja vu
            if option == 2:
                # Extraire les videos-id deja vue
                seen_videos = []
                for k, v in history_videos_rating.items():
                    for video in v:
                        seen_videos.append(video['doc_id'])

                all_videos_not_seen = _doc_topics_distribution_interest[~_doc_topics_distribution_interest['doc_id'].isin(seen_videos)]
                top_n = all_videos_not_seen.sort_values(by=['distance'], ascending=True)[0:top]

            # On elimine tous le videos dislike
            if option == 3:
                dislike_seen_videos = []
                for k, v in history_videos_rating.items():
                    for video in v:
                        if video['videoRating'] != 'aime':
                            dislike_seen_videos.append(video['doc_id'])

                all_videos_not_seen = _doc_topics_distribution_interest[~_doc_topics_distribution_interest['doc_id'].isin(dislike_seen_videos)]
                top_n = all_videos_not_seen.sort_values(by=['distance'], ascending=True)[0:top]

            # On elimine tous le videos like
            if option == 4:
                like_seen_videos = []
                for k, v in history_videos_rating.items():
                    for video in v:
                        if video['videoRating'] == 'aime':
                            like_seen_videos.append(video['doc_id'])

                all_videos_not_seen = _doc_topics_distribution_interest[~_doc_topics_distribution_interest['doc_id'].isin(like_seen_videos)]
                top_n = all_videos_not_seen.sort_values(by=['distance'], ascending=True)[0:top]

        return self._videos_infos[self._videos_infos['doc_id'].isin(top_n['doc_id'].to_numpy())]

    def _manhattan_distance(self, a, b):
        return sum(abs(e1 - e2) for e1, e2 in zip(a, b))

    # Simply return list of topics id
    def _build_cold_start_choices(self):
        columns = self._doc_topics_distribution.columns
        choices = columns[1:].to_numpy()
        return choices

    def get_cold_start_choices(self):
        return self._cold_start_choices

    def get_cold_start_videos(self, user_cold_start_position, top=5):
        top_n = self._doc_topics_distribution.sort_values(by=[user_cold_start_position], ascending=False)[0:top]
        res = self._videos_infos[self._videos_infos['doc_id'].isin(top_n['doc_id'].to_numpy())]
        return res

    def get_doc_topic_distribution(self):
        return self._doc_topics_distribution
