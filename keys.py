import os
import base64

spotify_token = os.getenv("SPOTIFY_TOKEN")
spotify_user_id = os.getenv("SPOTIFY_USER_ID")
spotify_secret = os.getenv("SPOTIFY_SECRET")

musix_match_secret = os.getenv("MUSIX_MATCH_SECRET")
app_secret_key = os.getenv("APP_SECRET_KEY")

id_secret = spotify_user_id+':'+spotify_secret
id_secret_64 = str(base64.b64encode(id_secret.encode('utf-8')))[1:].strip('\'')