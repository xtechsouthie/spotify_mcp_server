import spotipy
from spotipy.oauth2 import SpotifyPKCE
import json
import os
from dotenv import load_dotenv

load_dotenv()

#### This file is made for testing responses of them spotipy func

def test_response():
    auth_manager = SpotifyPKCE(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope="playlist-read-private user-read-playback-state user-modify-playback-state user-follow-read"
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    user = sp.current_user()
    playlists = sp.transfer_playback(device_id="##")
    print("Current user:\n")
    print(json.dumps(playlists, indent=2))
    
    # if playlists['items']:
    #     playlist_id = playlists['items'][0]['id']
    #     tracks = sp.playlist_tracks(playlist_id, limit=1)
    #     print("\nPLAYLIST TRACKS RESPONSE:")
    #     print(json.dumps(tracks, indent=2))

if __name__ == "__main__":
    test_response()