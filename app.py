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
    style={
        "display": "flex",
        "flex-direction": "column",
        "justify-content": "space-between",
        "align-items": "center",
        "gap": "1rem",
        "backgroundColor": colors["white"],
    },
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
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "center",
                        "align-items": "center",
                    },
                    children=[
                        html.Img(
                            id="image",
                            style={
                                "box-shadow": "10px 10px 5px grey",
                            },
                        ),
                        html.Br(),
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
                    style={
                        "display": "grid",
                        "grid-template-columns": "repeat(auto-fill, minmax(16rem, 1fr))",
                        "grid-auto-rows": "1fr",
                        "grid-gap": "1rem",
                    },
                    children=[
                        html.Div(
                            id="danceability-card",
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "background-color": colors["black"],
                                "border-radius": "8px",
                                "padding": "1rem",
                                "box-shadow": "10px 10px 5px grey",
                            },
                            children=[
                                html.Div(
                                    style={
                                        "font-size": "1.15rem",
                                        "text-align": "center",
                                        "color": colors["pink"],
                                    },
                                    children="DANCEABILITY",
                                ),
                                html.Div(
                                    id="danceability-card-value",
                                    style={
                                        "font-size": "2.3rem",
                                        "text-align": "center",
                                        "color": colors["pink"],
                                    },
                                ),
                                html.Div(
                                    id="danceability-card-description",
                                    children=audio_feature_description("danceability"),
                                    style={
                                        "text-align": "center",
                                        "margin-top": "auto",
                                        "margin-bottom": "auto",
                                        "color": colors["white"],
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            id="valence-card",
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "background-color": colors["black"],
                                "border-radius": "8px",
                                "padding": "1rem",
                                "box-shadow": "10px 10px 5px grey",
                            },
                            children=[
                                html.Div(
                                    style={
                                        "font-size": "1.15rem",
                                        "text-align": "center",
                                        "color": colors["pink"],
                                    },
                                    children="VALENCE",
                                ),
                                html.Div(
                                    id="valence-card-value",
                                    style={
                                        "font-size": "2.3rem",
                                        "text-align": "center",
                                        "color": colors["pink"],
                                    },
                                ),
                                html.Div(
                                    id="valence-card-description",
                                    children=audio_feature_description("valence"),
                                    style={
                                        "text-align": "center",
                                        "margin-top": "auto",
                                        "margin-bottom": "auto",
                                        "color": colors["white"],
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            id="energy-card",
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "background-color": colors["black"],
                                "border-radius": "8px",
                                "padding": "1rem",
                                "box-shadow": "10px 10px 5px grey",
                            },
                            children=[
                                html.Div(
                                    style={
                                        "font-size": "1.15rem",
                                        "text-align": "center",
                                        "color": colors["pink"],
                                    },
                                    children="ENERGY",
                                ),
                                html.Div(
                                    id="energy-card-value",
                                    style={
                                        "font-size": "2.3rem",
                                        "text-align": "center",
                                        "color": colors["pink"],
                                    },
                                ),
                                html.Div(
                                    id="energy-card-description",
                                    children=audio_feature_description("energy"),
                                    style={
                                        "text-align": "center",
                                        "margin-top": "auto",
                                        "margin-bottom": "auto",
                                        "color": colors["white"],
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            id="tempo-card",
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "background-color": colors["black"],
                                "border-radius": "8px",
                                "padding": "1rem",
                                "box-shadow": "10px 10px 5px grey",
                            },
                            children=[
                                html.Div(
                                    style={
                                        "font-size": "1.15rem",
                                        "text-align": "center",
                                        "color": colors["pink"],
                                    },
                                    children="TEMPO",
                                ),
                                html.Div(
                                    id="tempo-card-value",
                                    style={
                                        "font-size": "2.3rem",
                                        "text-align": "center",
                                        "color": colors["pink"],
                                    },
                                ),
                                html.Div(
                                    id="tempo-card-description",
                                    children=audio_feature_description("tempo"),
                                    style={
                                        "text-align": "center",
                                        "margin-top": "auto",
                                        "margin-bottom": "auto",
                                        "color": colors["white"],
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            id="loudness-card",
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "background-color": colors["black"],
                                "border-radius": "8px",
                                "padding": "1rem",
                                "box-shadow": "10px 10px 5px grey",
                            },
                            children=[
                                html.Div(
                                    style={
                                        "font-size": "1.15rem",
                                        "text-align": "center",
                                        "color": colors["pink"],
                                    },
                                    children="LOUDNESS",
                                ),
                                html.Div(
                                    id="loudness-card-value",
                                    style={
                                        "font-size": "2.3rem",
                                        "text-align": "center",
                                        "color": colors["pink"],
                                    },
                                ),
                                html.Div(
                                    id="loudness-card-description",
                                    children=audio_feature_description("loudness"),
                                    style={
                                        "text-align": "center",
                                        "margin-top": "auto",
                                        "margin-bottom": "auto",
                                        "color": colors["white"],
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            id="speechiness-card",
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "background-color": colors["black"],
                                "border-radius": "8px",
                                "padding": "1rem",
                                "box-shadow": "10px 10px 5px grey",
                            },
                            children=[
                                html.Div(
                                    style={
                                        "font-size": "1.15rem",
                                        "text-align": "center",
                                        "color": colors["pink"],
                                    },
                                    children="SPEECHINESS",
                                ),
                                html.Div(
                                    id="speechiness-card-value",
                                    style={
                                        "font-size": "2.3rem",
                                        "text-align": "center",
                                        "color": colors["pink"],
                                    },
                                ),
                                html.Div(
                                    id="speechiness-card-description",
                                    children=audio_feature_description("speechiness"),
                                    style={
                                        "text-align": "center",
                                        "margin-top": "auto",
                                        "margin-bottom": "auto",
                                        "color": colors["white"],
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            id="instrumentalness-card",
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "background-color": colors["black"],
                                "border-radius": "8px",
                                "padding": "1rem",
                                "box-shadow": "10px 10px 5px grey",
                            },
                            children=[
                                html.Div(
                                    style={
                                        "font-size": "1.15rem",
                                        "text-align": "center",
                                        "color": colors["pink"],
                                    },
                                    children="INSTRUMENTALNESS",
                                ),
                                html.Div(
                                    id="instrumentalness-card-value",
                                    style={
                                        "font-size": "2.3rem",
                                        "text-align": "center",
                                        "color": colors["pink"],
                                    },
                                ),
                                html.Div(
                                    id="instrumentalness-card-description",
                                    children=audio_feature_description(
                                        "instrumentalness"
                                    ),
                                    style={
                                        "text-align": "center",
                                        "margin-top": "auto",
                                        "margin-bottom": "auto",
                                        "color": colors["white"],
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            id="liveness-card",
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "background-color": colors["black"],
                                "border-radius": "8px",
                                "padding": "1rem",
                                "box-shadow": "10px 10px 5px grey",
                            },
                            children=[
                                html.Div(
                                    style={
                                        "font-size": "1.15rem",
                                        "text-align": "center",
                                        "color": colors["pink"],
                                    },
                                    children="LIVENESS",
                                ),
                                html.Div(
                                    id="liveness-card-value",
                                    style={
                                        "font-size": "2.3rem",
                                        "text-align": "center",
                                        "color": colors["pink"],
                                    },
                                ),
                                html.Div(
                                    id="liveness-card-description",
                                    children=audio_feature_description("liveness"),
                                    style={
                                        "text-align": "center",
                                        "margin-top": "auto",
                                        "margin-bottom": "auto",
                                        "color": colors["white"],
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            id="acousticness-card",
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "background-color": colors["black"],
                                "border-radius": "8px",
                                "padding": "1rem",
                                "box-shadow": "10px 10px 5px grey",
                            },
                            children=[
                                html.Div(
                                    style={
                                        "font-size": "1.15rem",
                                        "text-align": "center",
                                        "color": colors["pink"],
                                    },
                                    children="ACOUSTICNESS",
                                ),
                                html.Div(
                                    id="acousticness-card-value",
                                    style={
                                        "font-size": "2.3rem",
                                        "text-align": "center",
                                        "color": colors["pink"],
                                    },
                                ),
                                html.Div(
                                    id="acousticness-card-description",
                                    children=audio_feature_description("acousticness"),
                                    style={
                                        "text-align": "center",
                                        "margin-top": "auto",
                                        "margin-bottom": "auto",
                                        "color": colors["white"],
                                    },
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)


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
    if n_clicks == 0:
        raise exceptions.PreventUpdate
    uri = get_track_uri(query)
    if uri is None:
        return (
            {  # error-message style
                "display": "block",
                "color": "red",
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
    df = get_track_data(uri)
    if df.loc[0]["preview_url"] is not None:
        preview_src = df.loc[0]["preview_url"]
        preview_style = {
            "display": "block",
            "margin-top": "16px",
        }
    else:
        preview_src = ""
        preview_style = {
            "display": "none",
        }
    return (
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
