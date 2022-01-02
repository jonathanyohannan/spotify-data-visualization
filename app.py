from dash import (
    Dash,
    dcc,
    html,
    Input,
    Output,
    State,
    no_update,
    exceptions,
)
from functions import (
    get_track_uri,
    get_track_data,
    audio_feature_description,
)


colors = {
    "green": "#1db954",
    "white": "#ffffff",
    "black": "#191414",
    "pink": "#e246ab",
}

app = Dash(
    __name__,
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0",
        }
    ],
)
server = app.server
app.title = "Spotify Data Visualizer"

app.layout = html.Div(
    id="container",
    children=[
        html.H1(
            children="Spotify Data Visualizer",
            style={
                "color": colors["green"],
                "text-align": "center",
            },
        ),
        html.Div(
            children="Search for any track to learn about its audio features. Data is pulled from the Spotify API.",
            style={
                "text-align": "center",
            },
        ),
        html.A(
            children="Source Code",
            href="https://github.com/jonathanyohannan/spotify-data-visualization/",
            style={
                "color": colors["green"],
                "text-align": "center",
            },
        ),
        dcc.Input(
            id="query-input",
            placeholder="Search for a track",
            type="text",
            value="",
        ),
        html.Button(
            id="submit-button",
            n_clicks=0,
            children="Submit",
            style={
                "color": colors["white"],
                "background-color": colors["green"],
                "border": "none",
                "border-radius": "4px",
            },
        ),
        html.Div(
            id="error-message",
            children="No results found",
            style={
                "display": "none",
            },
        ),
        html.Div(
            id="output-container",
            style={"display": "none"},
            children=[
                html.Div(
                    id="metadata-container",
                    children=[
                        html.Img(
                            id="image",
                            style={
                                "box-shadow": "10px 10px 5px grey",
                                "margin-bottom": "1rem",
                            },
                        ),
                        html.Div(id="name"),
                        html.Div(id="artist"),
                        html.Div(id="album"),
                        html.Audio(
                            id="preview",
                            controls=True,
                        ),
                    ],
                ),
                html.Div(
                    id="cards-container",
                    children=[
                        html.Div(
                            id="danceability-card",
                            className="card",
                            children=[
                                html.Div(
                                    className="card-label",
                                    children="DANCEABILITY",
                                ),
                                html.Div(
                                    id="danceability-card-value",
                                    className="card-value",
                                ),
                                html.Div(
                                    className="card-description",
                                    children=audio_feature_description("danceability"),
                                ),
                            ],
                        ),
                        html.Div(
                            id="valence-card",
                            className="card",
                            children=[
                                html.Div(
                                    className="card-label",
                                    children="VALENCE",
                                ),
                                html.Div(
                                    id="valence-card-value",
                                    className="card-value",
                                ),
                                html.Div(
                                    className="card-description",
                                    children=audio_feature_description("valence"),
                                ),
                            ],
                        ),
                        html.Div(
                            id="energy-card",
                            className="card",
                            children=[
                                html.Div(
                                    className="card-label",
                                    children="ENERGY",
                                ),
                                html.Div(
                                    id="energy-card-value",
                                    className="card-value",
                                ),
                                html.Div(
                                    className="card-description",
                                    children=audio_feature_description("energy"),
                                ),
                            ],
                        ),
                        html.Div(
                            id="tempo-card",
                            className="card",
                            children=[
                                html.Div(
                                    className="card-label",
                                    children="TEMPO",
                                ),
                                html.Div(
                                    id="tempo-card-value",
                                    className="card-value",
                                ),
                                html.Div(
                                    className="card-description",
                                    children=audio_feature_description("tempo"),
                                ),
                            ],
                        ),
                        html.Div(
                            id="loudness-card",
                            className="card",
                            children=[
                                html.Div(
                                    className="card-label",
                                    children="LOUDNESS",
                                ),
                                html.Div(
                                    id="loudness-card-value",
                                    className="card-value",
                                ),
                                html.Div(
                                    className="card-description",
                                    children=audio_feature_description("loudness"),
                                ),
                            ],
                        ),
                        html.Div(
                            id="speechiness-card",
                            className="card",
                            children=[
                                html.Div(
                                    className="card-label",
                                    children="SPEECHINESS",
                                ),
                                html.Div(
                                    id="speechiness-card-value",
                                    className="card-value",
                                ),
                                html.Div(
                                    className="card-description",
                                    children=audio_feature_description("speechiness"),
                                ),
                            ],
                        ),
                        html.Div(
                            id="instrumentalness-card",
                            className="card",
                            children=[
                                html.Div(
                                    className="card-label",
                                    children="INSTRUMENTALNESS",
                                ),
                                html.Div(
                                    id="instrumentalness-card-value",
                                    className="card-value",
                                ),
                                html.Div(
                                    className="card-description",
                                    children=audio_feature_description(
                                        "instrumentalness"
                                    ),
                                ),
                            ],
                        ),
                        html.Div(
                            id="liveness-card",
                            className="card",
                            children=[
                                html.Div(
                                    className="card-label",
                                    children="LIVENESS",
                                ),
                                html.Div(
                                    id="liveness-card-value",
                                    className="card-value",
                                ),
                                html.Div(
                                    className="card-description",
                                    children=audio_feature_description("liveness"),
                                ),
                            ],
                        ),
                        html.Div(
                            id="acousticness-card",
                            className="card",
                            children=[
                                html.Div(
                                    className="card-label",
                                    children="ACOUSTICNESS",
                                ),
                                html.Div(
                                    id="acousticness-card-value",
                                    className="card-value",
                                ),
                                html.Div(
                                    className="card-description",
                                    children=audio_feature_description("acousticness"),
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)


# called when submit-button is clicked, query taken from query-input
@app.callback(
    Output(component_id="error-message", component_property="style"),
    Output(component_id="output-container", component_property="style"),
    Output(component_id="image", component_property="src"),
    Output(component_id="name", component_property="children"),
    Output(component_id="artist", component_property="children"),
    Output(component_id="album", component_property="children"),
    Output(component_id="preview", component_property="src"),
    Output(component_id="preview", component_property="style"),
    Output(component_id="danceability-card-value", component_property="children"),
    Output(component_id="valence-card-value", component_property="children"),
    Output(component_id="energy-card-value", component_property="children"),
    Output(component_id="tempo-card-value", component_property="children"),
    Output(component_id="loudness-card-value", component_property="children"),
    Output(component_id="speechiness-card-value", component_property="children"),
    Output(component_id="instrumentalness-card-value", component_property="children"),
    Output(component_id="liveness-card-value", component_property="children"),
    Output(component_id="acousticness-card-value", component_property="children"),
    Input(component_id="submit-button", component_property="n_clicks"),
    State(component_id="query-input", component_property="value"),
)
def update_output(n_clicks, query):
    if n_clicks == 0:  # at start of app, don't update anything
        raise exceptions.PreventUpdate
    uri = get_track_uri(query)  # search Spotify using query
    if uri is None:  # display error message if no results found for query
        return (
            {  # error-message style
                "display": "block",
                "color": "red",
                "text-align": "center",
            },
            no_update,  # output-container style
            no_update,  # image src
            no_update,  # name children
            no_update,  # artist children
            no_update,  # album children
            no_update,  # preview src
            no_update,  # preview style
            no_update,  # danceability-card-value children
            no_update,  # valence-card-value children
            no_update,  # energy-card-value children
            no_update,  # tempo-card-value children
            no_update,  # loudness-card-value children
            no_update,  # speechiness-card-value children
            no_update,  # instrumentalness-card-value children
            no_update,  # liveness-card-value children
            no_update,  # acousticness-card-value children
        )
    df = get_track_data(uri)  # get metadata and audio features for track
    if df.loc[0]["preview_url"] is not None:  # check if track has a preview
        preview_src = df.loc[0]["preview_url"]
        preview_style = {
            "display": "block",
            "margin-top": "1rem",
        }
    else:
        preview_src = ""
        preview_style = {
            "display": "none",
        }
    return (  # update output
        {  # error-message style
            "display": "none",
        },
        {  # output-container style
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "center",
            "align-items": "center",
            "gap": "1rem",
        },
        df.loc[0]["image"],  # image src
        df.loc[0]["name"],  # name children
        "by {}".format(df.loc[0]["artist"]),  # artist children
        "on {}".format(df.loc[0]["album"]),  # album children
        preview_src,  # preview src
        preview_style,  # preview style
        "{}".format(df.loc[0]["danceability"]),  # danceability-card-value children
        "{}".format(df.loc[0]["valence"]),  # valence-card-value children
        "{}".format(df.loc[0]["energy"]),  # energy-card-value children
        "{}".format(df.loc[0]["tempo"]),  # tempo-card-value children
        "{}".format(df.loc[0]["loudness"]),  # loudness-card-value children
        "{}".format(df.loc[0]["speechiness"]),  # speechiness-card-value children
        "{}".format(
            df.loc[0]["instrumentalness"]
        ),  # instrumentalness-card-value children
        "{}".format(df.loc[0]["liveness"]),  # liveness-card-value children
        "{}".format(df.loc[0]["acousticness"]),  # acousticness-card-value children
    )


if __name__ == "__main__":
    app.run_server(debug=True)
