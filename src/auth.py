import os
import spotipy
import sys
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
                scope="playlist-read-private "          
                  "playlist-read-collaborative "      
                  "playlist-modify-private "         
                  "playlist-modify-public "          
                  "user-read-playback-state "        
                  "user-modify-playback-state "     
                  "user-library-read "              
                  "user-library-modify "           
                  "user-top-read "                   
                  "user-follow-read "                
                  "user-read-email "                 
                  "user-read-private "              
                  "streaming"      
            )
            self.client = spotipy.Spotify(auth_manager=auth_manager)

            #testing connection
            user = self.client.current_user()
            print(f"Authenticated currently as {user['display_name']}", file=sys.stderr)
        except Exception as e:
            print(f"Authentication failed: {e}", file=sys.stderr)
            self.client = None

    def get_client(self):
        return self.client
    
spotify_auth = SpotifyAuth()

