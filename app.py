from process import CreatePlaylist
import requests
import time, logging
from flask import Flask, render_template, make_response, redirect, request, session, url_for
from helpers import generateRandomString, get_tokens
from urllib.parse import urlencode
from secrets import spotify_user_id, redirect_uri, scope, secret_key

app = Flask(__name__)
app.secret_key = secret_key

#todo
#display home before running function
#handle timeout

@app.route('/')
def index():
    if 'token' in session:
        nr = CreatePlaylist()
        tracks = nr.process(session['token'])
        return render_template('home.html',token=session['token'])
    else:
        return render_template('index.html')

@app.route('/login')
def login():
    state = generateRandomString(16)
    session['state_key'] = state

    authorize_url = "https://accounts.spotify.com/authorize?"
    params = {'response_type': 'code', 'redirect_uri': redirect_uri, 'scope': scope, 'client_id': spotify_user_id, 'state': state}
    query_params = urlencode(params)
    
    response = make_response(redirect(authorize_url + query_params))
    return response

@app.route('/callback') #spotify will redirect to this route. set as redirect_uri.
def callback():
    #check if passed state via url equals to stored state or if url passes error var
    if request.args.get('state') != session['state_key'] or request.args.get('error'):
        return render_template('index.html', error='State failed.')

    else:
        code = request.args.get('code')
        session.pop('state', None)  
    
        payload = get_tokens(code)
        if payload != None:
            session['token'] = payload[0]
            session['refresh_token'] = payload[1]
            session['token_expiration'] = time.time() + payload[2]
        else:
            return render_template('error.html', error='Failed to access token')
    print(session)
    # current_user = getUserInformation(session)
    # session['user_id'] = current_user['id']
    # logging.info('new user: '+ session['user_id'])

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    [session.pop(key) for key in list(session.keys())] #clear session before officially logging out via spotify's link
    return redirect("https://accounts.spotify.com/logout")
