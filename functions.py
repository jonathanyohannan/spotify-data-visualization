import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from base64 import b64encode


colors = {
    "green": "#1db954",
    "white": "#ffffff",
    "black": "#191414",
    "pink": "#e246ab",
}


# Client ID and secret needed to access the Spotify API (client credentials flow).
c_id = os.environ.get("SPOTIPY_CLIENT_ID")
c_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
c_credentials_manager = SpotifyClientCredentials(client_id=c_id, client_secret=c_secret)
sp = spotipy.Spotify(client_credentials_manager=c_credentials_manager)


# Search for a track and return its Spotify URI.
# Returns None if the query is empty or if there are no results found for the query.
def get_track_uri(query):
    if query == "":
        return None
    results = sp.search(q=query, type="track")
    try:
        return results["tracks"]["items"][0]["uri"]
    except IndexError:
        return None


# Get the metadata and audio features of a track provided its Spotify URI.
# Returns a pandas dataframe.
def get_audio_features(track_uri):
    metadata = sp.track(track_id=track_uri)
    audio_features = sp.audio_features(tracks=track_uri)
    return pd.DataFrame(
        data=[
            [
                metadata["name"],
                metadata["album"]["artists"][0]["name"],
                metadata["album"]["name"],
                metadata["album"]["images"][1]["url"],
                metadata["preview_url"],
                audio_features[0]["danceability"],
                audio_features[0]["valence"],
                audio_features[0]["energy"],
                audio_features[0]["tempo"],
                audio_features[0]["loudness"],
                audio_features[0]["speechiness"],
                audio_features[0]["instrumentalness"],
                audio_features[0]["liveness"],
                audio_features[0]["acousticness"],
            ]
        ],
        columns=[
            "name",
            "artist",
            "album",
            "image",
            "preview_url",
            "danceability",
            "valence",
            "energy",
            "tempo",
            "loudness",
            "speechiness",
            "instrumentalness",
            "liveness",
            "acousticness",
        ],
    )


# Get the audio analysis of a track provided its Spotify URI.
# Creates a waveform using Plotly Graph Objects, then uses b64encode to return the graph as a static image.
def get_audio_analysis(track_uri):
    audio_analysis = sp.audio_analysis(track_id=track_uri)
    duration = audio_analysis["track"]["duration"]
    segments = audio_analysis["segments"]
    segments_map = np.zeros(shape=(len(segments), 3))
    i = 0
    for segment in segments:
        segment_start = segment["start"] / duration
        segment_duration = segment["duration"] / duration
        segment_loudness = 1 - (min(max(segment["loudness_max"], -35), 0) / -35)
        segments_map[i] = [segment_start, segment_duration, segment_loudness]
        i += 1
    maximum = np.amax(segments_map, axis=0)[2]
    levels = []
    for i in range(0, 1000, 1):
        for segment in segments_map:
            if segment[0] <= i / 1000 <= segment[0] + segment[1] and i % 8 == 0:
                loudness = segment[2] / maximum
                levels.append([i, loudness / 2, -loudness / 2])
                break
    df = pd.DataFrame(levels, columns=["index", "upper_bound", "lower_bound"])
    trace1 = go.Bar(
        x=df["index"],
        y=df["upper_bound"],
        marker_color=colors["pink"],
        marker_line_width=0,
    )
    trace2 = go.Bar(
        x=df["index"],
        y=df["lower_bound"],
        marker_color=colors["pink"],
        marker_line_width=0,
    )
    data = [trace1, trace2]
    layout = go.Layout(
        barmode="overlay",
        showlegend=False,
        xaxis=dict(
            showticklabels=False,
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
        plot_bgcolor=colors["black"],
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
        ),
    )
    fig = go.Figure(data=data, layout=layout)
    img_bytes = fig.to_image(format="png")
    encoding = b64encode(img_bytes).decode()
    img_b64 = "data:image/png;base64," + encoding
    return img_b64


# Returns descriptions of the different audio features provided in the Spotify API.
def audio_feature_description(feature):
    if feature == "danceability":
        return "Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable."
    elif feature == "valence":
        return "A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry)."
    elif feature == "energy":
        return "Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy."
    elif feature == "tempo":
        return "The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration."
    elif feature == "loudness":
        return "The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db."
    elif feature == "speechiness":
        return "Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks."
    elif feature == "instrumentalness":
        return 'Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.'
    elif feature == "liveness":
        return "Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live."
    elif feature == "acousticness":
        return "A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic."
    else:
        return None
