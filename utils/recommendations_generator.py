import pandas as pd


from utils.lda_reader import LDAReader
from config.CONSTANTS import *

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

            if choice['topic'] == cold_start_position:
                probability = 1.0

            res['cold_start'].append({
                choice['topic']: probability
            })

        return res

    def calculate_center_of_interest(self, videos_rating, current_user_area_interest, option=CALCULATE_CI_OPTION):
        # Creer liste des videos like et dislike
        liked_videos = []
        disliked_videos = []
        for k, v in videos_rating.items():
            for video in v:
                if video['videoRating'] == 'aime':
                    liked_videos.append(video['doc_id'])
                else:
                    disliked_videos.append(video['doc_id'])

        liked_videos = list(set(liked_videos))
        disliked_videos = list(set(disliked_videos))
        # Calcule preliminaire pour la distribution moyenne des videos regardes
        if len(liked_videos) > 0:
            liked_videos_topic_distribution = self._doc_topics_distribution[self._doc_topics_distribution['doc_id'].isin(liked_videos)]
            liked_videos_topic_distribution = liked_videos_topic_distribution[liked_videos_topic_distribution.columns.drop(['doc_id'])]
            liked_videos_topic_distribution_sum = liked_videos_topic_distribution.sum()
            liked_videos_topic_distribution_mean = liked_videos_topic_distribution_sum / len(liked_videos)

        if len(disliked_videos) > 0:
            disliked_videos_topic_distribution = self._doc_topics_distribution[self._doc_topics_distribution['doc_id'].isin(disliked_videos)]
            disliked_videos_topic_distribution = disliked_videos_topic_distribution[disliked_videos_topic_distribution.columns.drop(['doc_id'])]
            disliked_videos_topic_distribution_sum = disliked_videos_topic_distribution.sum()
            disliked_videos_topic_distribution_mean = disliked_videos_topic_distribution_sum / len(disliked_videos)

        # On considere seulement les videos : like
        _user_area_of_interest=None
        if option == 1:
            if len(liked_videos) > 0:
                _user_area_of_interest = liked_videos_topic_distribution_mean.to_frame().transpose()
            # Si aucun videos n'a ete aime, on ne change pas le centre d'interet
            else:
                pass

        # On considere les videos : like et dislike
        elif option == 2:
            # E0) Calcul des valeurs moyennes des 2 categories de video (like, dislike)
            if len(liked_videos) > 0 and len(disliked_videos) > 0:
                # E1) Calcul de la difference par topic entre les distributions like et dislike
                diff = liked_videos_topic_distribution_mean - disliked_videos_topic_distribution_mean
                # E2) Additionne la difference aux videos like
                liked_videos_plus_diff = liked_videos_topic_distribution_mean + diff
                # E3) Recherche des valeurs negatives, les replacer par 0 et
                # distribuer uniformement la somme de ces valeurs (les negatives) sur toutes les
                # autres composantes du vecteur.
                if liked_videos_plus_diff.min() < 0:
                    _user_area_of_interest = self._evenly_distribute_negative_value(liked_videos_plus_diff=liked_videos_plus_diff)
                else:
                    _user_area_of_interest = liked_videos_plus_diff.to_frame().transpose()

            elif len(liked_videos) > 0 and len(disliked_videos) == 0:
                _user_area_of_interest = liked_videos_topic_distribution_mean.to_frame().transpose()

            # Aucune video n'a ete aime
            # Si l'utilisateur n'aime aucun video en cold start, selon ce calcul, son nouveau centre d'interet restera le meme
            else:
                user_last_are_interest = current_user_area_interest
                topic_ids = []
                proba = []
                for val in user_last_are_interest:
                    topic_ids.append(list(val.keys())[0])
                    proba.append(list(val.values())[0])

                df_user_last_are_interest = pd.DataFrame(proba, index=topic_ids)

                # E1) Calcul de la difference par topic entre les distributions centre interet et dislike
                # le .sum(1) sert uniquement a transformer la de df en format pour la soustraction
                df_user_last_are_interest = df_user_last_are_interest.sum(1)
                diff = df_user_last_are_interest - disliked_videos_topic_distribution_mean

                # E2) Additionne la difference aux videos like
                liked_videos_plus_diff = df_user_last_are_interest + diff

                # E3) Recherche des valeurs negatives, les replacer par 0 et
                # distribuer uniformement la somme de ces valeurs (les negatives) sur toutes les
                # autres composantes du vecteur.
                if liked_videos_plus_diff.min() < 0:
                    _user_area_of_interest = self._evenly_distribute_negative_value(liked_videos_plus_diff=liked_videos_plus_diff)
                    # _user_area_of_interest = _user_area_of_interest.to_frame().transpose()
                else:
                    _user_area_of_interest = liked_videos_plus_diff.to_frame().transpose()

        print(_user_area_of_interest.sum(1))

        return _user_area_of_interest

    def _evenly_distribute_negative_value(self, liked_videos_plus_diff):
        negative_value = liked_videos_plus_diff[liked_videos_plus_diff < 0]
        negative_value_topic_id = negative_value.keys().to_list()
        total_topic = len(liked_videos_plus_diff)  # norme du vecteur
        value_to_distribute = (negative_value.sum()) / (total_topic - len(negative_value_topic_id))

        _user_area_of_interest = liked_videos_plus_diff + value_to_distribute
        for topic_id in negative_value_topic_id:
            _user_area_of_interest[topic_id] = 0

        loop_counter = 0
        while _user_area_of_interest.min() < 0:

            negative_value = _user_area_of_interest[_user_area_of_interest < 0]
            _list = negative_value.keys().to_list()
            for key in _list:
                negative_value_topic_id.append(key)

            value_to_distribute = (negative_value.sum()) / (total_topic - len(negative_value_topic_id))

            _user_area_of_interest = liked_videos_plus_diff + value_to_distribute
            for topic_id in negative_value_topic_id:
                _user_area_of_interest[topic_id] = 0

            # Check if sum equal to 1
            if _user_area_of_interest.sum() > 1.0:
                value_to_distribute = (_user_area_of_interest.sum() - 1) / (total_topic - len(negative_value_topic_id))
                _user_area_of_interest = _user_area_of_interest - value_to_distribute
                for topic_id in negative_value_topic_id:
                    _user_area_of_interest[topic_id] = 0

            loop_counter += 1
            print('loop_counter : ' + str(loop_counter))

        # Reshape result
        return _user_area_of_interest.to_frame().transpose()


    def get_new_recommendations(self, user_area_of_interest, option=NEW_REC_OPTION,
                                top=TOP_N_VIDEOS, history_videos_rating=None, do_normalization=True):

        _doc_topics_distribution_interest = pd.DataFrame()
        _is_recommendation_ended = False

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

        # Application de la normalisation
        if do_normalization:
            _doc_topics_distribution_interest = self._normalize_doc_topics_distribution_interest(_doc_topics_distribution_interest)

        # On considere seulement le centre d'interet
        if option == 1:
            top_n = _doc_topics_distribution_interest.sort_values(by=['distance'], ascending=True)[0:top]

        # Serie d'options pour ne pas recommander des videos deja recommandees
        elif history_videos_rating:
            # On elimine tous les videos deja vu
            if option == 2:
                # Extraire les videos-id deja vue
                seen_videos = []
                for k, v in history_videos_rating.items():
                    for video in v:
                        seen_videos.append(video['doc_id'])

                all_videos_not_seen = _doc_topics_distribution_interest[~_doc_topics_distribution_interest['doc_id'].isin(seen_videos)]
                top_n = all_videos_not_seen.sort_values(by=['distance'], ascending=True)[0:top]

            # On elimine tous les videos dislike
            if option == 3:
                dislike_seen_videos = []
                for k, v in history_videos_rating.items():
                    for video in v:
                        if video['videoRating'] != 'aime pas':
                            dislike_seen_videos.append(video['doc_id'])

                all_videos_not_seen = _doc_topics_distribution_interest[~_doc_topics_distribution_interest['doc_id'].isin(dislike_seen_videos)]
                top_n = all_videos_not_seen.sort_values(by=['distance'], ascending=True)[0:top]

            # On elimine tous les videos like
            if option == 4:
                like_seen_videos = []
                for k, v in history_videos_rating.items():
                    for video in v:
                        if video['videoRating'] == 'aime':
                            like_seen_videos.append(video['doc_id'])

                all_videos_not_seen = _doc_topics_distribution_interest[~_doc_topics_distribution_interest['doc_id'].isin(like_seen_videos)]
                top_n = all_videos_not_seen.sort_values(by=['distance'], ascending=True)[0:top]

            if option == 5:
                seen_videos = []
                for k, v in history_videos_rating.items():
                    for video in v:
                        seen_videos.append(video['doc_id'])

                # Applique la selection du le seuil
                top_videos_by_threshold = _doc_topics_distribution_interest[_doc_topics_distribution_interest['distance'] <= RECOMMENDATION_THRESHOLD_MIN]
                all_videos_not_seen = top_videos_by_threshold[~top_videos_by_threshold['doc_id'].isin(seen_videos)]
                top_n = all_videos_not_seen.sort_values(by=['distance'], ascending=True)[0:top]

                if len(top_n) == 0:
                    top_n = top_videos_by_threshold.sort_values(by=['distance'], ascending=True)[0:top]
                    _is_recommendation_ended = True
                    print('END OF NEW REC')

        print(top_n)
        # Ajout la bd => rec_and_distance
        response = self._format_recommendations(doc_ids=top_n['doc_id'].to_numpy(), recommendation_ended=_is_recommendation_ended)
        return response, top_n['distance'].to_numpy()

    def _format_recommendations(self, doc_ids, recommendation_ended=False):

        return_val = {'recommendations': [], 'recommendation_ended': recommendation_ended}
        for id in doc_ids:
            info = self._videos_infos[self._videos_infos['doc_id'] == id]
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

    def _manhattan_distance(self, a, b):
        return sum(abs(e1 - e2) for e1, e2 in zip(a, b))

    def _normalize_doc_topics_distribution_interest(self, data):
        min = data['distance'].min()
        max = data['distance'].max()
        data['distance'] = (data['distance'] - min) / (max - min)
        return data


    # Simply return list of topics id
    def _build_cold_start_choices(self):
        #columns = self._doc_topics_distribution.columns
        #choices = columns[1:].to_numpy()
        x = self._lda_reader.get_topic_terms_distribution()
        choices = []
        for col in x.columns:
            choices.append({'topic': col, 'topic_id': col.strip('t_'), 'terms': x[col].to_list()})
        return choices

    def get_cold_start_choices(self):
        return self._cold_start_choices

    def get_cold_start_videos(self, user_cold_start_position, top=TOP_N_VIDEOS_COLD_START):
        top_n = self._doc_topics_distribution.sort_values(by=[user_cold_start_position], ascending=False)[0:top]
        return self._format_recommendations(doc_ids=top_n['doc_id'].to_numpy())

    def get_doc_topic_distribution(self):
        return self._doc_topics_distribution
