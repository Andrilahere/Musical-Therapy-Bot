import os
import traceback
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth


load_dotenv()


# Spotify configs
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
username='wy5ae8pvx9sifldc8zffsntap'


scope = [
    'user-read-playback-state',
    'user-modify-playback-state',
    'user-read-private',
    'playlist-read-private',
    'playlist-read-collaborative',
    'streaming'
]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                     client_secret=client_secret, redirect_uri=redirect_uri, scope=scope, username=username
    ))


# Spotify functions
def add_song_to_queue(song_uri: str):
    try:
        sp.add_to_queue(song_uri)
        return "Added track to queue successfully"
    except:
        return "Error adding track to queue"


def find_song_by_name(name: str):
    results = sp.search(q=name, type='track')
    if (results):
        song_uri = results['tracks']['items'][0]['uri']
        return song_uri


def find_song_by_lyrics(lyrics: str):
    results = sp.search(q=f"lyrics:{lyrics}", type='track')
    if (results):
        if len(results['tracks']['items']) > 0:
            song_uri = results['tracks']['items'][0]['uri']
            return song_uri
        else:
            return ("No matching tracks found")


def add_song_to_queue_by_song_name(song_name: str):
    song_uri = find_song_by_name(song_name)
    if (song_uri):
        add_song_to_queue(song_uri)
        return "Successfully added song to queue"
    else:
        return "No matching tracks found"


def add_song_to_queue_by_lyrics(lyrics: str):
    song_uri = find_song_by_lyrics(lyrics)
    if (song_uri):
        return add_song_to_queue(song_uri)
    else:
        return "No matching tracks found"


def start_playing_song_by_name(song_name: str):
    song_uri = find_song_by_name(song_name)
    try:
        if (song_uri):
            sp.start_playback(uris=[song_uri])
            return f"Started playing song {song_name}"
    except Exception as e:
        error_message = traceback.format_exc()  # Get the formatted error message
        return f"Couldn't play song. Error: {error_message}"


def start_playing_song_by_lyrics(lyrics: str):
    song_uri = find_song_by_lyrics(lyrics)
    if (song_uri):
        sp.start_playback(uris=[song_uri])
        return f"Started playing song with lyrics: {lyrics}"
    else:
        return "No matching tracks found"


def start_playlist_by_name(playlist_name: str):
    """This defaults to playing the current user's playlist"""
    results = sp.search(q=playlist_name, type="playlist", limit=1)

    if results and results["playlists"]["items"]:
        playlist_uri = results["playlists"]["items"][0]["uri"]
        sp.start_playback(context_uri=playlist_uri)
        return ("Playlist started:", playlist_name)
    else:
        return ("Playlist not found.")
    
def start_private_playlist_by_name(playlist_name: str):
    """Start a private playlist owned or followed by the user."""
    try:
        
        playlists = sp.current_user_playlists()
        
        
        for playlist in playlists['items']:
            if playlist['name'].lower() == playlist_name.lower():
                playlist_uri = playlist['uri']
                sp.start_playback(context_uri=playlist_uri)
                return f"Private playlist '{playlist_name}' started successfully!"
        
        return f"Private playlist '{playlist_name}' not found in your library."
    
    except Exception as e:
        error_message = traceback.format_exc()
        return f"An error occurred: {error_message}"



def start_music():
    try:
        sp.start_playback()
        return "Playback started!"
    except:
        return "Error starting playback. Make sure to wake the player up before starting."


def pause_music():
    try:
        sp.pause_playback()
        return "Playback paused!"
    except:
        return "Error pausing playback. Make sure to wake the player up before stopping."


def next_track():
    try:
        sp.next_track()
        return "Successfully skipped to the next track."
    except spotipy.client.SpotifyException as e:
        return ("Error occurred while skipping track:", e)


def previous_track():
    try:
        sp.previous_track()
        return "Successfully went back to the previous track."
    except Exception as e:
        error_message = traceback.format_exc()  # Get the formatted error message
        return f"Error occurred while going back to the previous track: {error_message}"
