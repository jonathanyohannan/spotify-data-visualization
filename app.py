import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = os.environ.get("SPOTIPY_CLIENT_ID")
client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
