import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
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

colors = {
    "background": "#121212",
    "green-text": "#19d660",
    "white-text": "#ffffff",
    "pink-text": "#e6299f",
}

app = dash.Dash(__name__)
app.title = "Spotify Data Visualizer"

app.layout = html.Div(
    id="container",
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
        html.Div(
            children="View in-depth audio analysis of all tracks from the Tame Impala discography. Data is retrieved using the Spotify API.",
            style={
                "color": colors["white-text"],
                "text-align": "center",
                "width": "33%",
            },
        ),
        html.Br(),
        html.A(
            children="Source Code",
            href="https://github.com/jonathanyohannan/spotify-data-visualization",
            style={"color": colors["pink-text"]},
        ),
        html.Br(),
        dcc.RadioItems(
            id="radio-items",
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
        dcc.Graph(id="bar-graph"),
        html.Div(
            id="y-value-description",
            style={
                "color": colors["white-text"],
                "text-align": "center",
                "width": "33%",
            },
        ),
        html.Br(),
        html.Div(
            children="Designed by Jonathan Yohannan",
            style={"color": colors["pink-text"]},
        ),
    ],
)


@app.callback(
    Output(component_id="bar-graph", component_property="figure"),
    Output(component_id="y-value-description", component_property="children"),
    Input(component_id="radio-items", component_property="value"),
)
def update_figure(selection):
    fig = px.bar(
        data_frame=df,
        x="name",
        y=selection,
        color="album",
        color_discrete_sequence=["#2ca8b0", "#f17934", "#614b6a", "#920e05"],
    )
    fig.update_layout(
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        font_color=colors["green-text"],
    )
    fig.update_xaxes(title_text="song", showticklabels=False)

    if selection == "danceability":
        description = "Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable."
    elif selection == "valence":
        description = "A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry)."
    elif selection == "energy":
        description = "Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy."
    elif selection == "tempo":
        description = "The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration."
    elif selection == "loudness":
        description = "The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db."
    elif selection == "speechiness":
        description = "Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks."
    elif selection == "instrumentalness":
        description = 'Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.'

    return fig, description


if __name__ == "__main__":
    app.run_server(debug=True)
