import random, string, requests, time
from config import id_secret_64, app_callback_url, spotify_get_token_url, spotify_get_user_url


def generate_random_string(N):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))


def get_tokens(code):
    authorization = 'Basic {}'.format(id_secret_64)

    headers = {
        'Authorization': authorization, 'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body = {'code': code, 'redirect_uri': app_callback_url, 'grant_type': 'authorization_code'}
    post_response = requests.post(spotify_get_token_url, headers=headers, data=body)

    if post_response.status_code == 200:
        res_json = post_response.json()
        return res_json['access_token'], res_json['refresh_token'], res_json['expires_in']
    else:
        return None


def get_user_information(session):
    payload = make_get_request(session, spotify_get_user_url)

    if payload is not None:
        return None

    return payload


def make_get_request(session, url, params={}):
    headers = {'Authorization': 'Bearer {}'.format(session['token'])}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401 and check_token_status(session) is not None:
        return make_get_request(session, url, params)
    else:
        return None


def check_token_status(session):
    if time.time() > session['token_expiration']:
        payload = refresh_token(session['refresh_token'])

        if payload is not None:
            session['token'] = payload[0]
            session['token_expiration'] = time.time() + payload[1]
        else:
            return None

    return 'Success'


def refresh_token(token):
    authorization = 'Basic {}'.format(id_secret_64)

    headers = {
        'Authorization': authorization, 'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    body = {'refresh_token': token, 'grant-type': 'refresh_token'}
    post_response = requests.post(spotify_get_token_url, headers=headers, data=body)

    if post_response.status_code == 200:
        json = post_response.json()
        return json['access_token'], json['expires_in']
    else:
        return None
