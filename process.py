import json
import requests
from polyglot.detect import Detector
from textblob import TextBlob

from secrets import spotify_token, spotify_user_id, musix_key

def get_songs():
    query = "https://api.spotify.com/v1/me/tracks?limit=20"
    response = requests.get(
        query,
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(spotify_token)
        }
    )
    print(response.status_code)
    response_json = response.json()   
    res = [{'track':item["track"]["name"],'artist':item["track"]["artists"][0]["name"]} for item in response_json["items"]]

    return res

def get_lyrics():
    # track = track_data['track']
    # artist = track_data['artist']
    track = 'ナイロンの糸'.replace(" ","%20")
    artist = 'sakanaction'.replace(" ","%20")

    query = "https://api.musixmatch.com/ws/1.1/matcher.lyrics.get?format=json&callback=callback&q_track={}&q_artist={}&apikey={}".format(track,artist,musix_key)
    response = requests.get(query)
    res = json.loads(response.text)
    res_text = res['message']['body']['lyrics']['lyrics_body']
    lyrics = "\n".join(res_text.split('\n\n')[:2])
    b = TextBlob(lyrics)
    lang = b.detect_language()
    

def process():
    track_data = get_songs()
    x = map(get_lyrics, track_data)
    print(x)
    for items in track_data:
        print(items)


if __name__ == '__main__':
    print(get_songs())