from flask import Flask, render_template, make_response, redirect
import process
import requests
from urllib.parse import urlencode
from secrets import spotify_user_id, redirect_uri, state

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    authorize_url = "https://accounts.spotify.com/authorize?"
    params = {'response_type': 'code', 'redirect_uri': redirect_uri, 'scope': 'user-read-private', 'client_id': spotify_user_id, 'state': state}
    query_params = urlencode(params)
    response = make_response(redirect(authorize_url + query_params))
    return response
    
