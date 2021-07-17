import base64

spotify_token = ''
spotify_user_id = ''
spotify_secret = ''
musix_key = ''
secret_key = ""

id_secret = spotify_user_id+':'+spotify_secret
id_secret_64 = str(base64.b64encode(id_secret.encode('utf-8')))[1:].strip('\'')