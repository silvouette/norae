import json
import requests
from textblob import TextBlob
from textblob.exceptions import TranslatorError
from config import musix_match_secret, musix_match_lang_detector_url_format, spotify_get_tracks_url


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
        response_json = response.json()
        # store track's id, uri, name, and array of artists
        res = [{'id': item["track"]["id"], 'uri': item["track"]["uri"], 'track': item["track"]["name"],
                'artist': [artist["name"] for artist in item["track"]["artists"]]} for item in response_json["items"]]

        return res

    def get_lang(self, track_data):  # find each track's language by detecting its lyrics' language
        track = track_data['track'].replace(" ", "%20")
        artist = track_data['artist'][0].replace(" ", "%20")

        query = musix_match_lang_detector_url_format.format(track, artist, musix_match_secret)
        response = requests.get(query)
        res = json.loads(response.text)

        if response.status_code == 200:
            res_text = res['message']['body']['lyrics']['lyrics_body']  # store lyrics
            lyrics = "\n".join(res_text.split('\n\n')[:2])  # take only first 2 paragraphs of the lyrics

            try:
                text_blob = TextBlob(lyrics)
                track_data['lang'] = text_blob.detect_language()
            except TranslatorError:
                track_data['lang'] = 'none'

        return track_data

    def process(self, token):
        # get list of saved tracks
        track_data = self.get_songs(token)
        # get and store language of each tracks
        track_lang = list(map(self.get_lang, track_data))
        # get unique languages from list for grouping purpose later
        unique_lang = list(dict.fromkeys(val['lang'] for val in track_lang))
        # group tracks based on lang
        group = [{'lang': lang, 'tracks': [item for item in track_lang if item['lang'] == lang]} for lang in
                 unique_lang]
        return group
