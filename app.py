
from flask import Flask, request, url_for, session, redirect, render_template
from pagesetup import setup, finish
import config
import time
import spotipy
import os
from song import Song

from spotipy.oauth2 import SpotifyOAuth


app = Flask(__name__)

app.secret_key = config.APP_SECRET
app.config['SESSION_COOKIE_NAME'] = 'JSpotify Cookie'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    sp_oauth = sp()
    auth_url = sp_oauth.get_authorize_url() 

    print("auth url: " + auth_url)
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = sp()
    code = request.args.get('code')
    session.pop("token_info", None)  # Remove any existing token info in session
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    print("Access token:", session['token_info']['access_token'])
    print("Refresh token:", session['token_info']['refresh_token'])

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
        session['token_info'] = token_info
    return token_info 

@app.route('/Tracks')
def Tracks():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect("/")
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_tracks = sp.current_user_top_tracks(50, 0, "short_term")
    songs = [Song(track['name'], track['popularity'], i+1, track['artists'][0]['name']) for i, track in enumerate(top_tracks['items'])]
    # Pass the list of song names to the template
    intervals = {
    "1-10": 0, "11-20": 0, "21-30": 0, "31-40": 0, "41-50": 0,
    "51-60": 0, "61-70": 0, "71-80": 0, "81-90": 0, "91-100": 0
    }
    for song in songs:
        popularity = song.popularity
        lower_bound = ((popularity - 1) // 10) * 10 + 1
        upper_bound = lower_bound + 9
        interval_key = f"{lower_bound}-{upper_bound}"
        intervals[interval_key] += 1
    labels = list(intervals.keys())
    counts = list(intervals.values())
    return render_template('test.html', songs=songs, labels=labels, counts=counts)



@app.route('/logout')
def logout():
    session.clear()
    cache_path = '.cache'
    if os.path.exists(cache_path):
        os.remove(cache_path)
    return redirect('/')

def sp():
    return SpotifyOAuth(
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET,
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read user-top-read",
        show_dialog=True)

