from process import CreatePlaylist
from helpers import refreshToken
import time
from flask import Flask, render_template, make_response, redirect, request, session, url_for
from helpers import generateRandomString, get_tokens, checkTokenStatus, getUserInformation
from urllib.parse import urlencode
from secrets import spotify_user_id, secret_key

app = Flask(__name__)
app.secret_key = secret_key

@app.route('/')
def index():
    #direct to home only if session exists and not expired, else direct to login.
    if 'token' in session and checkTokenStatus(session)=='Success':
        return render_template('home.html',token=session['token'])
    else:
        return render_template('index.html')

@app.route('/playlists')
def playlists():
    if 'token' in session and checkTokenStatus(session)=='Success':
        nr = CreatePlaylist()
        tracks = nr.process(session['token'])
        return render_template('playlists.html', grouped_tracks=tracks, token=session['token'], u_id=session['user_id'])
    else:
        return render_template('index.html')

@app.route('/login')
def login():
    state = generateRandomString(16)
    session['state_key'] = state
    redirect_uri = 'http://127.0.0.1:5000/callback'
    scope = 'user-read-private user-library-read playlist-read-private playlist-modify-public playlist-modify-private'

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
            return render_template('index.html', error='Failed to access token')
    current_user = getUserInformation(session)
    session['user_id'] = current_user['id']

    return redirect(url_for('index'))

@app.route('/refresh', methods=['GET'])
def refresh():
    payload = refreshToken(session['refresh_token'])
    if payload != None:
            session['token'] = payload[0]
            session['token_expiration'] = time.time() + payload[1]
    return 'success'

@app.route('/logout')
def logout():
    [session.pop(key) for key in list(session.keys())] #clear session before officially logging out via spotify's link
    return redirect("https://accounts.spotify.com/logout")
