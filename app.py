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
                "color": colors["pink"],
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
                                "padding": "8%",
                            },
                            children=[
                                html.P(id="name"),
                                html.P(id="artist"),
                                html.P(id="album"),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    id="danceability-container",
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                        "justify-content": "space-evenly",
                        "align-items": "center",
                    },
                    children=[
                        dcc.Graph(
                            id="danceability-graph",
                            style={
                                "flex": "1 1 0",
                            },
                        ),
                        html.P(
                            id="danceability-description",
                            children=audio_feature_description(feature="danceability"),
                            style={
                                "flex": "1 1 0",
                                "color": colors["white"],
                                "text-align": "center",
                            },
                        ),
                    ],
                ),
                html.Div(
                    id="valence-container",
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                        "justify-content": "space-evenly",
                        "align-items": "center",
                    },
                    children=[
                        dcc.Graph(
                            id="valence-graph",
                            style={
                                "flex": "1 1 0",
                            },
                        ),
                        html.P(
                            id="valence-description",
                            children=audio_feature_description(feature="valence"),
                            style={
                                "flex": "1 1 0",
                                "color": colors["white"],
                                "text-align": "center",
                            },
                        ),
                    ],
                ),
                html.Div(
                    id="energy-container",
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                        "justify-content": "space-evenly",
                        "align-items": "center",
                    },
                    children=[
                        dcc.Graph(
                            id="energy-graph",
                            style={
                                "flex": "1 1 0",
                            },
                        ),
                        html.P(
                            id="energy-description",
                            children=audio_feature_description(feature="energy"),
                            style={
                                "flex": "1 1 0",
                                "color": colors["white"],
                                "text-align": "center",
                            },
                        ),
                    ],
                ),
                html.Div(
                    id="tempo-container",
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                        "justify-content": "space-evenly",
                        "align-items": "center",
                    },
                    children=[
                        dcc.Graph(
                            id="tempo-graph",
                            style={
                                "flex": "1 1 0",
                            },
                        ),
                        html.P(
                            id="tempo-description",
                            children=audio_feature_description(feature="tempo"),
                            style={
                                "flex": "1 1 0",
                                "color": colors["white"],
                                "text-align": "center",
                            },
                        ),
                    ],
                ),
                html.Div(
                    id="loudness-container",
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                        "justify-content": "space-evenly",
                        "align-items": "center",
                    },
                    children=[
                        dcc.Graph(
                            id="loudness-graph",
                            style={
                                "flex": "1 1 0",
                            },
                        ),
                        html.P(
                            id="loudness-description",
                            children=audio_feature_description(feature="loudness"),
                            style={
                                "flex": "1 1 0",
                                "color": colors["white"],
                                "text-align": "center",
                            },
                        ),
                    ],
                ),
                html.Div(
                    id="speechiness-container",
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                        "justify-content": "space-evenly",
                        "align-items": "center",
                    },
                    children=[
                        dcc.Graph(
                            id="speechiness-graph",
                            style={
                                "flex": "1 1 0",
                            },
                        ),
                        html.P(
                            id="speechiness-description",
                            children=audio_feature_description(feature="speechiness"),
                            style={
                                "flex": "1 1 0",
                                "color": colors["white"],
                                "text-align": "center",
                            },
                        ),
                    ],
                ),
                html.Div(
                    id="instrumentalness-container",
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                        "justify-content": "space-evenly",
                        "align-items": "center",
                    },
                    children=[
                        dcc.Graph(
                            id="instrumentalness-graph",
                            style={
                                "flex": "1 1 0",
                            },
                        ),
                        html.P(
                            id="instrumentalness-description",
                            children=audio_feature_description(
                                feature="instrumentalness"
                            ),
                            style={
                                "flex": "1 1 0",
                                "color": colors["white"],
                                "text-align": "center",
                            },
                        ),
                    ],
                ),
                html.Div(
                    id="liveness-container",
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                        "justify-content": "space-evenly",
                        "align-items": "center",
                    },
                    children=[
                        dcc.Graph(
                            id="liveness-graph",
                            style={
                                "flex": "1 1 0",
                            },
                        ),
                        html.P(
                            id="liveness-description",
                            children=audio_feature_description(feature="liveness"),
                            style={
                                "flex": "1 1 0",
                                "color": colors["white"],
                                "text-align": "center",
                            },
                        ),
                    ],
                ),
                html.Div(
                    id="acousticness-container",
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                        "justify-content": "space-evenly",
                        "align-items": "center",
                    },
                    children=[
                        dcc.Graph(
                            id="acousticness-graph",
                            style={
                                "flex": "1 1 0",
                            },
                        ),
                        html.P(
                            id="acousticness-description",
                            children=audio_feature_description(feature="acousticness"),
                            style={
                                "flex": "1 1 0",
                                "color": colors["white"],
                                "text-align": "center",
                            },
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
    Output(component_id="danceability-graph", component_property="figure"),
    Output(component_id="valence-graph", component_property="figure"),
    Output(component_id="energy-graph", component_property="figure"),
    Output(component_id="tempo-graph", component_property="figure"),
    Output(component_id="loudness-graph", component_property="figure"),
    Output(component_id="speechiness-graph", component_property="figure"),
    Output(component_id="instrumentalness-graph", component_property="figure"),
    Output(component_id="liveness-graph", component_property="figure"),
    Output(component_id="acousticness-graph", component_property="figure"),
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
        )
    df = get_track_data(uri)
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
        df.loc[0]["name"],
        "by {}".format(df.loc[0]["artist"]),
        "on {}".format(df.loc[0]["album"]),
        create_graph(dataframe=df, variable="danceability"),
        create_graph(dataframe=df, variable="valence"),
        create_graph(dataframe=df, variable="energy"),
        create_graph(dataframe=df, variable="tempo"),
        create_graph(dataframe=df, variable="loudness"),
        create_graph(dataframe=df, variable="speechiness"),
        create_graph(dataframe=df, variable="instrumentalness"),
        create_graph(dataframe=df, variable="liveness"),
        create_graph(dataframe=df, variable="acousticness"),
    )


if __name__ == "__main__":
    app.run_server(debug=True)
