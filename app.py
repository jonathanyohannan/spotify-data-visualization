import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd


c_id = os.environ.get("SPOTIPY_CLIENT_ID")
c_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")

c_credentials_manager = SpotifyClientCredentials(client_id=c_id, client_secret=c_secret)
sp = spotipy.Spotify(client_credentials_manager=c_credentials_manager)

# Get track IDs from playlist
# Playlist is a public playlist I have created with all tracks from every studio album by Tame Impala
# Spotify URL: https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF?si=ab299c75b0ed405c
track_ids = []
playlist = sp.playlist(
    playlist_id="https://open.spotify.com/playlist/0oxqEzWZEDFVBfcfBQf3CC?si=b8b691e2c4024b93"
)
for item in playlist["tracks"]["items"]:
    track = item["track"]
    track_ids.append(track["id"])

# Get metadata and audio features for each track
# danceability: Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
# valence: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).
# energy: Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.
# tempo: The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.
# loudness: The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db.
# speechiness: Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.
# instrumentalness: Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.
tracks = []
for track_id in track_ids:
    metadata = sp.track(track_id)
    audio_features = sp.audio_features(track_id)
    name = metadata["name"]
    artist = metadata["album"]["artists"][0]["name"]
    album = metadata["album"]["name"]
    # mood
    danceability = audio_features[0]["danceability"]
    valence = audio_features[0]["valence"]
    energy = audio_features[0]["energy"]
    tempo = audio_features[0]["tempo"]
    # properties
    loudness = audio_features[0]["loudness"]
    speechiness = audio_features[0]["speechiness"]
    instrumentalness = audio_features[0]["instrumentalness"]
    # put it all together
    track = [
        name,
        artist,
        album,
        danceability,
        valence,
        energy,
        tempo,
        loudness,
        speechiness,
        instrumentalness,
    ]
    tracks.append(track)

# Enter track data into pandas dataframe
df = pd.DataFrame(
    tracks,
    columns=[
        "name",
        "artist",
        "album",
        "danceability",
        "valence",
        "energy",
        "tempo",
        "loudness",
        "speechiness",
        "instrumentalness",
    ],
)

app = dash.Dash(__name__)

colors = {"background": "#121212", "green-text": "#19d660", "white-text": "#ffffff"}

fig = px.bar(data_frame=df, x="name", y="danceability", color="album")
fig.update_layout(
    plot_bgcolor=colors["background"],
    paper_bgcolor=colors["background"],
    font_color=colors["green-text"],
)

app.layout = html.Div(
    style={
        "display": "flex",
        "flex-direction": "column",
        "justify-content": "space=between",
        "align-items": "center",
        "backgroundColor": colors["background"],
    },
    children=[
        html.H1(
            children="Spotify Data Visualizer",
            style={"color": colors["green-text"]},
        ),
        dcc.RadioItems(
            options=[
                {"label": "Danceability", "value": "danceability"},
                {"label": "Valence", "value": "valence"},
                {"label": "Energy", "value": "energy"},
                {"label": "Tempo", "value": "tempo"},
                {"label": "Loudness", "value": "loudness"},
                {"label": "Speechiness", "value": "speechiness"},
                {"label": "Instrumentalness", "value": "instrumentalness"},
            ],
            value="danceability",
            style={
                "display": "flex",
                "flex-direction": "row:",
                "justify-content": "space-evenly",
                "color": colors["green-text"],
            },
        ),
        dcc.Graph(id="example-graph", figure=fig),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
