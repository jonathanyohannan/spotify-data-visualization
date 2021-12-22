import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


c_id = os.environ.get("SPOTIPY_CLIENT_ID")
c_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")

c_credentials_manager = SpotifyClientCredentials(client_id=c_id, client_secret=c_secret)
sp = spotipy.Spotify(client_credentials_manager=c_credentials_manager)

# Spotify URL: https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF?si=ab299c75b0ed405c
track_ids = []
playlist = sp.playlist(
    playlist_id="https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF?si=ab299c75b0ed405c"
)
for item in playlist["tracks"]["items"]:
    track = item["track"]
    track_ids.append(track["id"])
