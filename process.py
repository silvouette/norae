import json
import requests
import threading
from textblob import TextBlob
from config import musix_match_secret, musix_match_lang_detector_url_format, spotify_get_tracks_url


def _collect_songs(spotify_response):
    songs = []

    for item in spotify_response["items"]:
        artists = []

        for artist in item["track"]["artists"]:
            artists.append(artist["name"])

        songs.append({
            'id': item["track"]["id"],
            'uri': item["track"]["uri"],
            'track': item["track"]["name"],
            'artist': artists
        })

    return songs


def _collect_languages(clazz, track_data):
    track_languages = []
    track_language_jobs = []

    for data in track_data:
        job = threading.Thread(target=lambda: track_languages.append(clazz.get_lang(data)))
        job.start()
        track_language_jobs.append(job)

    for job in track_language_jobs:
        job.join()

    return track_languages


class CreatePlaylist:
    def __init__(self):
        pass

    def get_songs(self, spotify_token):  # get user's saved tracks from spotify
        response = requests.get(
            spotify_get_tracks_url,
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(spotify_token)
            }
        )

        # store track's id, uri, name, and array of artists
        return _collect_songs(response.json())

    def get_lang(self, track_data):  # find each track's language by detecting its lyrics' language
        track = track_data['track'].replace(" ", "%20")
        artist = track_data['artist'][0].replace(" ", "%20")

        query = musix_match_lang_detector_url_format.format(track, artist, musix_match_secret)
        track_data['lang'] = 'none'

        try:
            response = requests.get(query)
            res = json.loads(response.text)

            res_text = res['message']['body']['lyrics']['lyrics_body']  # store lyrics
            lyrics = "\n".join(res_text.split('\n\n')[:2])  # take only first 2 paragraphs of the lyrics

            text_blob = TextBlob(lyrics)
            track_data['lang'] = text_blob.detect_language()
        except Exception:
            pass

        return track_data

    def process(self, token):
        # get list of saved tracks
        track_data = self.get_songs(token)

        # collect all track languages
        track_languages = _collect_languages(self, track_data)

        # get unique languages from list for grouping purpose later
        unique_lang = list(dict.fromkeys(val['lang'] for val in track_languages))

        # group tracks based on lang
        return [{
            'lang': lang,
            'tracks': [item for item in track_languages if item['lang'] == lang]
        } for lang in unique_lang]
