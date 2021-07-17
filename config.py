import os
import base64

app_host = os.getenv("APP_HOST", "")
app_secret_key = os.getenv("APP_SECRET_KEY", "")
app_callback_url = "{}/callback".format(app_host)

spotify_token = os.getenv("SPOTIFY_TOKEN", "")
spotify_user_id = os.getenv("SPOTIFY_USER_ID", "")
spotify_secret = os.getenv("SPOTIFY_SECRET", "")

musix_match_secret = os.getenv("MUSIX_MATCH_SECRET", "")

id_secret = spotify_user_id + ':' + spotify_secret
id_secret_64 = str(base64.b64encode(id_secret.encode('utf-8')))[1:].strip('\'')

spotify_get_token_url = 'https://accounts.spotify.com/api/token'
spotiy_get_tracks_url = "https://api.spotify.com/v1/me/tracks?limit=20"

musix_match_lang_detector_url_format = "https://api.musixmatch.com/ws/1.1/matcher.lyrics.get?format=json&callback" \
                                       "=callback&q_track={}&q_artist={}&apikey={}"
