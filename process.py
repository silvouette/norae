import json
import requests
from textblob import TextBlob
from secrets import musix_key
# todo:
# button to save made playlist

class CreatePlaylist:
    def __init__(self):
        print("Program started")

    def get_songs(self, spotify_token): #get user's saved tracks from spotify
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
        #store track's id, uri, name, and array of artists  
        res = [{'id':item["track"]["id"],'uri':item["track"]["uri"],'track':item["track"]["name"],'artist':[artist["name"] for artist in item["track"]["artists"]]} for item in response_json["items"]]

        return res

    def get_lang(self, track_data): #find each track's language by detecting its lyrics' language
        track = track_data['track'].replace(" ","%20")
        artist = track_data['artist'][0].replace(" ","%20")

        query = "https://api.musixmatch.com/ws/1.1/matcher.lyrics.get?format=json&callback=callback&q_track={}&q_artist={}&apikey={}".format(track,artist,musix_key)
        response = requests.get(query)
        res = json.loads(response.text)
        if res['message']['header']['status_code'] == 200:
            res_text = res['message']['body']['lyrics']['lyrics_body'] #store lyrics
            lyrics = "\n".join(res_text.split('\n\n')[:2]) #take only first 2 paragraphs of the lyrics
        else:
            lyrics = ""
        if lyrics:
            b = TextBlob(lyrics)
            lang = b.detect_language()
        else:
            lang = "none" #fallback value in case track's lyrics isn't in musixmatch db or if the track is instrumental
        
        track_data['lang'] = lang
        return track_data

    def process(self, token):
        #get list of saved tracks
        track_data = self.get_songs(token)
        #get and store language of each tracks
        track_lang = list(map(self.get_lang, track_data))
        #get unique languages from list for grouping purpose later
        unique_lang = list(dict.fromkeys(val['lang'] for val in track_lang))
        #group tracks based on lang
        group = [{'lang':lang,'tracks':[item for item in track_lang if item['lang']==lang]} for lang in unique_lang]
        return group
        
# if __name__ == '__main__':
#     nr = CreatePlaylist()
#     nr.process(spotify_user_id)