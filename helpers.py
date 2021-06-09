import random, string, json, requests, logging, time
from secrets import id_secret_64

def generateRandomString(N):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

def get_tokens(code):
    redirect_uri = 'http://127.0.0.1:5000/callback'
    scope = 'user-read-private user-library-read playlist-modify-public'
    authorization = 'Basic {}'.format(id_secret_64)
    token_url = 'https://accounts.spotify.com/api/token'
    
    headers = {
        'Authorization':authorization, 'Accept':'application/json', 
        'Content-Type':'application/x-www-form-urlencoded'
    }
    body = {'code':code, 'redirect_uri':redirect_uri, 'grant_type': 'authorization_code'}
    post_response = requests.post(token_url, headers=headers, data=body)

    if post_response.status_code == 200:
        res_json = post_response.json()
        print(res_json)
        return res_json['access_token'], res_json['refresh_token'], res_json['expires_in']
    else:
        logging.error('getToken:' + str(post_response.status_code))
        return None

def getUserInformation(session):
    url = 'https://api.spotify.com/v1/me'
    payload = makeGetRequest(session,url)

    if payload==None:
        return None
    
    return payload

def makeGetRequest(session,url,params={}):
    headers = {'Authorization':'Bearer {}'.format(session['token'])}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401 and checkTokenStatus(session) != None:
        return makeGetRequest(session, url, params)
    else:
        logging.error('makeGetRequest:' + str(response.status_code))
        return None

def checkTokenStatus(session):
    if time.time() > session['token_expiration']:
        payload = refreshToken(session['refresh_token'])
    
        if payload != None:
            session['token'] = payload[0]
            session['token_expiration'] = time.time() + payload[1]
        else:
            logging.error('checkTokenStatus')
            return None
            
    return 'Success'

def refreshToken(refresh_token):
    token_url = 'https://accounts.spotify.com/api/token'
    authorization = 'Basic {}'.format(id_secret_64) 

    headers = {
        'Authorization':authorization, 'Accept':'application/json', 
        'Content-Type':'application/x-www-form-urlencoded' 
    }
    body = {'refresh_token':refresh_token, 'grant-type':'refresh_token'}
    post_response = requests.post(token_url, headers=headers, data=body)

    if post_response.status_code == 200:
        json = post_response.json()
        return json['access_token'], json['expires_in']
    else:
        logging.error('refreshToken:' + str(post_response.status_code))
        return None
