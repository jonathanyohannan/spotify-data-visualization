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
    create_graph,
    audio_feature_description,
)


colors = {
    "green": "#1db954",
    "white": "#ffffff",
    "black": "#191414",
    "pink": "#e246ab",
}

app = Dash(__name__)
server = app.server
app.title = "Spotify Data Visualizer"

app.layout = html.Div(
    id="container",
    style={
        "display": "flex",
        "flex-direction": "column",
        "justify-content": "space=between",
        "align-items": "center",
        "backgroundColor": colors["black"],
    },
    children=[
        html.H1(
            children="Spotify Data Visualizer",
            style={
                "color": colors["green"],
            },
        ),
        html.P(
            children="Search for any track to learn about its audio features. Data is pulled from the Spotify API.",
        ),
        html.A(
            children="Source Code",
            href="https://github.com/jonathanyohannan/spotify-data-visualization/",
            style={
                "color": colors["green"],
            },
        ),
        html.Br(),
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
        html.P(
            id="error-message",
            children="No results found",
            style={
                "display": "none",
            },
        ),
        html.Br(),
        html.Div(
            id="output-container",
            style={"display": "none"},
            children=[
                html.Div(
                    id="metadata-container",
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                        "justify-content": "space-evenly",
                        "align-items": "center",
                        "color": colors["white"],
                    },
                    children=[
                        html.Img(id="image"),
                        html.Div(
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "justify-content": "space-between",
                                "align-items": "flex-start",
                                "padding": "16px",
                            },
                            children=[
                                html.P(id="name"),
                                html.P(id="artist"),
                                html.P(id="album"),
                                html.Audio(
                                    id="preview",
                                    controls=True,
                                ),
                            ],
                        ),
                    ],
                ),
                html.Br(),
                html.Div(
                    id="cards",
                    style={
                        "display": "grid",
                        "grid-template-columns": "repeat(3, minmax(300px, 1fr))",
                        "grid-auto-rows": "1fr",
                        "grid-gap": "1em",
                    },
                    children=[
                        html.Div(
                            id="danceability-card",
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "background-color": "#000000",
                                "border-radius": "8px",
                                "padding": "0.5em",
                            },
                            children=[
                                html.Div(
                                    id="danceability-card-value",
                                    style={
                                        "font-size": "2em",
                                        "color": colors["pink"],
                                        "margin-bottom": "auto",
                                    },
                                ),
                                html.Div(
                                    id="danceability-card-description",
                                    children=audio_feature_description("danceability"),
                                ),
                            ],
                        ),
                        html.Div(
                            id="valence-card",
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "background-color": "#000000",
                                "border-radius": "8px",
                                "padding": "0.5em",
                            },
                            children=[
                                html.Div(
                                    id="valence-card-value",
                                    style={
                                        "font-size": "2em",
                                        "color": colors["pink"],
                                        "margin-bottom": "auto",
                                    },
                                ),
                                html.Div(
                                    id="valence-card-description",
                                    children=audio_feature_description("valence"),
                                ),
                            ],
                        ),
                        html.Div(
                            id="energy-card",
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "background-color": "#000000",
                                "border-radius": "8px",
                                "padding": "0.5em",
                            },
                            children=[
                                html.Div(
                                    id="energy-card-value",
                                    style={
                                        "font-size": "2em",
                                        "color": colors["pink"],
                                        "margin-bottom": "auto",
                                    },
                                ),
                                html.Div(
                                    id="energy-card-description",
                                    children=audio_feature_description("energy"),
                                ),
                            ],
                        ),
                        html.Div(
                            id="tempo-card",
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "background-color": "#000000",
                                "border-radius": "8px",
                                "padding": "0.5em",
                            },
                            children=[
                                html.Div(
                                    id="tempo-card-value",
                                    style={
                                        "font-size": "2em",
                                        "color": colors["pink"],
                                        "margin-bottom": "auto",
                                    },
                                ),
                                html.Div(
                                    id="tempo-card-description",
                                    children=audio_feature_description("tempo"),
                                ),
                            ],
                        ),
                        html.Div(
                            id="loudness-card",
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "background-color": "#000000",
                                "border-radius": "8px",
                                "padding": "0.5em",
                            },
                            children=[
                                html.Div(
                                    id="loudness-card-value",
                                    style={
                                        "font-size": "2em",
                                        "color": colors["pink"],
                                        "margin-bottom": "auto",
                                    },
                                ),
                                html.Div(
                                    id="loudness-card-description",
                                    children=audio_feature_description("loudness"),
                                ),
                            ],
                        ),
                        html.Div(
                            id="speechiness-card",
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "background-color": "#000000",
                                "border-radius": "8px",
                                "padding": "0.5em",
                            },
                            children=[
                                html.Div(
                                    id="speechiness-card-value",
                                    style={
                                        "font-size": "2em",
                                        "color": colors["pink"],
                                        "margin-bottom": "auto",
                                    },
                                ),
                                html.Div(
                                    id="speechiness-card-description",
                                    children=audio_feature_description("speechiness"),
                                ),
                            ],
                        ),
                        html.Div(
                            id="instrumentalness-card",
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "background-color": "#000000",
                                "border-radius": "8px",
                                "padding": "0.5em",
                            },
                            children=[
                                html.Div(
                                    id="instrumentalness-card-value",
                                    style={
                                        "font-size": "2em",
                                        "color": colors["pink"],
                                        "margin-bottom": "auto",
                                    },
                                ),
                                html.Div(
                                    id="instrumentalness-card-description",
                                    children=audio_feature_description(
                                        "instrumentalness"
                                    ),
                                ),
                            ],
                        ),
                        html.Div(
                            id="liveness-card",
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "background-color": "#000000",
                                "border-radius": "8px",
                                "padding": "0.5em",
                            },
                            children=[
                                html.Div(
                                    id="liveness-card-value",
                                    style={
                                        "font-size": "2em",
                                        "color": colors["pink"],
                                        "margin-bottom": "auto",
                                    },
                                ),
                                html.Div(
                                    id="liveness-card-description",
                                    children=audio_feature_description("liveness"),
                                ),
                            ],
                        ),
                        html.Div(
                            id="acousticness-card",
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "background-color": "#000000",
                                "border-radius": "8px",
                                "padding": "0.5em",
                            },
                            children=[
                                html.Div(
                                    id="acousticness-card-value",
                                    style={
                                        "font-size": "2em",
                                        "color": colors["pink"],
                                        "margin-bottom": "auto",
                                    },
                                ),
                                html.Div(
                                    id="acousticness-card-description",
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


@app.callback(
    Output(component_id="error-message", component_property="style"),
    Output(component_id="output-container", component_property="style"),
    Output(component_id="image", component_property="src"),
    Output(component_id="preview", component_property="src"),
    Output(component_id="preview", component_property="style"),
    Output(component_id="name", component_property="children"),
    Output(component_id="artist", component_property="children"),
    Output(component_id="album", component_property="children"),
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
            {
                "display": "block",
                "color": "red",
            },
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
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
        {
            "display": "none",
        },
        {
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "space-evenly",
            "align-items": "center",
        },
        df.loc[0]["image"],
        preview_src,
        preview_style,
        df.loc[0]["name"],
        "by {}".format(df.loc[0]["artist"]),
        "on {}".format(df.loc[0]["album"]),
        "Danceability: {}".format(df.loc[0]["danceability"]),
        "Valence: {}".format(df.loc[0]["valence"]),
        "Energy: {}".format(df.loc[0]["energy"]),
        "Tempo: {}".format(df.loc[0]["tempo"]),
        "Loudness: {}".format(df.loc[0]["loudness"]),
        "Speechiness: {}".format(df.loc[0]["speechiness"]),
        "Instrumentalness: {}".format(df.loc[0]["instrumentalness"]),
        "Liveness: {}".format(df.loc[0]["liveness"]),
        "Acousticness: {}".format(df.loc[0]["acousticness"]),
    )


if __name__ == "__main__":
    app.run_server(debug=True)
