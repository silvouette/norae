import random, string, json, requests, logging, base64, time
from secrets import redirect_uri, spotify_user_id, spotify_secret

def generateRandomString(N):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

def get_tokens(code):
    id_secret = spotify_user_id+':'+spotify_secret
    id_secret_64 = str(base64.b64encode(id_secret.encode('utf-8')))[1:].strip('\'')
    authorization = 'Basic {}'.format(id_secret_64)
    token_url = 'https://accounts.spotify.com/api/token'
    
    headers = {
        'Authorization':authorization, 'Accept':'application/json', 
        'Content-Type':'application/x-www-form-urlencoded'
    }
    body = {'code':code, 'redirect_uri':redirect_uri, 'grant_type': 'authorization_code'}
    post_response = requests.post(token_url, headers=headers, data=body)
    print(post_response.json())
    if post_response.status_code == 200:
        res_json = post_response.json()
        print(res_json)
        return res_json['access_token'], res_json['refresh_token'], res_json['expires_in']
    else:
        logging.error('getToken:' + str(post_response.status_code))
        return None

# def getUserInformation(session):
#     url = 'https://api.spotify.com/v1/me'
#     payload = makeGetRequest(session,url)

#     if payload==None:
#         return None
    
#     return payload

# def makeGetRequest(session,url,params={}):
#     headers = {'Authorization':'Bearer {}'.format(session['token'])}
#     response = requests.get(url, headers=headers, params=params)

#     if response.status_code == 200:
#         return response.json()
#     elif response.status_code == 401 and checkTokenStatus(session) != None:
#         return makeGetRequest(session, url, params)
#     else:
#         logging.error('makeGetRequest:' + str(response.status_code))
#         return None

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
    id_secret = spotify_user_id+':'+spotify_secret
    id_secret_64 = str(base64.b64encode(id_secret.encode('utf-8')))[1:].strip('\'')
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
