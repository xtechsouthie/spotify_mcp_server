import spotipy
from spotipy.oauth2 import SpotifyPKCE
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_response():
    auth_manager = SpotifyPKCE(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope="playlist-read-private"
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    playlists = sp.current_user_playlists(limit=1)
    print("PLAYLISTS RESPONSE:")
    print(json.dumps(playlists, indent=2))
    
    if playlists['items']:
        playlist_id = playlists['items'][0]['id']
        tracks = sp.playlist_tracks(playlist_id, limit=1)
        print("\nPLAYLIST TRACKS RESPONSE:")
        print(json.dumps(tracks, indent=2))

if __name__ == "__main__":
    test_response()