# authentication.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

def get_spotify_client():
    """Authenticate with Spotify and return a Spotify client"""
    
   
    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
    
   
    SCOPE = "user-library-read playlist-read-private playlist-read-collaborative playlist-modify-public user-top-read user-read-playback-state streaming"
    

   
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        open_browser=True,
        cache_path=".spotify_cache"
    )
    spotify_client = spotipy.Spotify(auth_manager=auth_manager)
    try:
        user_info = spotify_client.current_user()
        print("Spotify authentication successful. User ID:", user_info['id'])
    except Exception as e:
        print("Authentication failed:", e)

    return spotify_client


