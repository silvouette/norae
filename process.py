import json
import requests
from textblob import TextBlob
from secrets import spotify_token, spotify_user_id, musix_key

# todo:
# get spotify auth
# group songs based on lang
# display made groups with list of songs
# button to save made playlist

class CreatePlaylist:
    def __init__(self):
        print("Program started")
        # get spotify auth

    def get_songs(self):
        query = "https://api.spotify.com/v1/me/tracks?limit=20"
        response = requests.get(
            query,
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(spotify_token)
            }
        )
        response_json = response.json()   
        res = [{'track':item["track"]["name"],'artist':item["track"]["artists"][0]["name"]} for item in response_json["items"]]

        return res

    def get_lang(self, track_data):
        track = track_data['track'].replace(" ","%20")
        artist = track_data['artist'].replace(" ","%20")

        query = "https://api.musixmatch.com/ws/1.1/matcher.lyrics.get?format=json&callback=callback&q_track={}&q_artist={}&apikey={}".format(track,artist,musix_key)
        response = requests.get(query)
        res = json.loads(response.text)
        res_text = res['message']['body']['lyrics']['lyrics_body']
        lyrics = "\n".join(res_text.split('\n\n')[:2]) #take only first 2 paragraphs of the lyrics
        if lyrics:
            b = TextBlob(lyrics)
            lang = b.detect_language()
        else:
            lang = "none"
        
        track_data['lang'] = lang
        return track_data

    def process(self):
        track_data = self.get_songs()
        track_data = map(self.get_lang, track_data)

if __name__ == '__main__':
    nr = CreatePlaylist()
    nr.process()