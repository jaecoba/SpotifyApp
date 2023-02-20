
from flask import Flask, request, url_for, session, redirect, render_template
from pagesetup import setup, finish
import config
import json
import time
import spotipy

from spotipy.oauth2 import SpotifyOAuth


app = Flask(__name__)

app.secret_key = config.APP_SECRET
app.config['SESSION_COOKIE_NAME'] = 'JSpotify Cookie'

setup()


@app.route('/')
def login():
    sp_oauth = sp()
    auth_url = sp_oauth.get_authorize_url() 
    print("auth url: " + auth_url)
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = sp()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect("/topTracks")

@app.route('/topTracks')
def topTracks():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    top = sp.current_user_top_tracks(50,0,"short_term")
    
    #opens html template, writes song list onto file
    file = open("test.html", "a+")
    file.write("\n<ol>")
    for song in top['items']:
        file.write("\n<li>" + song['name'] + "</li>")    

    file.write("\n</ol>")
    finish()
    return render_template('test.html')


# Checks to see if token is valid and gets a new token if not
def get_token():
    token_valid = True
    token_info = session.get("token_info", {})

    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    print("time: " + str(now))
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        sp_oauth = sp()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid

def sp():
    return SpotifyOAuth(
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET,
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read user-top-read")

