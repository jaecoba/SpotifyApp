
from flask import Flask, request, url_for, session, redirect, render_template
from pagesetup import setup, finish
import config
import time
import spotipy
import os

from spotipy.oauth2 import SpotifyOAuth


app = Flask(__name__)

app.secret_key = config.APP_SECRET
app.config['SESSION_COOKIE_NAME'] = 'JSpotify Cookie'



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
    return redirect("/Tracks")

def get_token():
    token_info = session.get("token_info", None)
    if not token_info: 
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60 
    if (is_expired): 
        sp_oauth = sp()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info 


@app.route('/Tracks')
def Tracks():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect("/")
    sp = spotipy.Spotify(auth=token_info['access_token'])
    top = sp.current_user_top_tracks(50,0,"short_term")
    user_top_songs = sp.current_user_top_tracks(
        limit = 50, 
        offset=0, 
        time_range="medium_term"
    )
    #opens html template, writes song list onto file

    setup()
    print("hello")
    file = open("test.html", "a+")
    file.write("\n<ol>")
    for song in top['items']:
        file.write("\n<li>" + song['name'] + "</li>")    
    file.write("\n</ol>")
    file.write("\n<h1>wop</h1>")
    finish()
    file.close()
    #file = open("test.html", "a+")

    return render_template('test.html')

# Checks to see if token is valid and gets a new token if not

def sp():
    return SpotifyOAuth(
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET,
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read user-top-read",
        show_dialog=True)

