import os
import spotipy
from spotipy.oauth2 import SpotifyPKCE
from dotenv import load_dotenv

load_dotenv()

class SpotifyAuth:
    def __init__(self):
        self.client = None
        self._initialize()

    def _initialize(self):
        try:
            auth_manager = SpotifyPKCE(
                client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
                scope="playlist-read-private playlist-modify-private playlist-modify-public "
                      "user-read-playback-state user-modify-playback-state user-library-read "
                      "user-library-modify streaming"
            )
            self.client = spotipy.Spotify(auth_manager=auth_manager)

            #testing connection
            user = self.client.current_user()
            print(f"Authenticated currently as {user["display_name"]}")
        except Exception as e:
            print(f"Authentication failed: {e}")
            self.client = None

    def get_client(self):
        return self.client
    
spotify_auth = SpotifyAuth()

