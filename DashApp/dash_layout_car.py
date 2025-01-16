from dash import html, dcc
import dash_bootstrap_components as dbc

param_speed = html.Div(
    [
        dbc.Label("speed *", html_for="param-speed"),
        dcc.Slider(min=0,max=100, step=10, value=0, id="param-speed")
    ],
    className="mb-3",
)

param_steering_angle = html.Div(
    [
        dbc.Label("steering angle", html_for="param-steering-angle"),
        dcc.Slider(min=45,max=135, step=5, id="param-steering-angle")
    ],
    className="mb-3",
)

param_time_forward = html.Div(
    [
        dbc.Label("time (forward)", html_for="param-time-forward"),
        dcc.Slider(min=0,max=30, step=5, id="param-time-forward")
    ],
    className="mb-3",
)

param_time_backward = html.Div(
    [
        dbc.Label("time (backward)", html_for="param-time-backward"),
        dcc.Slider(min=0,max=30, step=5, id="param-time-backward")
    ],
    className="mb-3",
)

param_time_stop = html.Div(
    [
        dbc.Label("time (stop)", html_for="param-time-stop"),
        dcc.Slider(min=0,max=30, step=5, id="param-time-stop")
    ],
    className="mb-3",
)

form_fahrmodus1 = dbc.Stack(
    [
        dbc.Row(
            [
                dbc.Col(param_speed)
            ]
        ),
        dbc.Row(
            [
                dbc.Col(param_time_forward),
                dbc.Col(param_time_backward),
                dbc.Col(param_time_stop)
            ]
        )
    ],
    gap=4
)               

content = dbc.Row(
    [
      dbc.Col(
        dbc.Stack(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Select(
                                placeholder="Fahrmodus",
                                id="my-select",
                                options=[
                                    {"label": "Fahrmodus 1", "value": "1"},
                                    {"label": "Fahrmodus 2", "value": "2"},
                                    {"label": "Fahrmodus 3", "value": "3"},
                                    {"label": "Fahrmodus 4", "value": "4"},
                                    {"label": "Fahrmodus 5", "value": "5"},
                                    {"label": "Fahrmodus 6", "value": "6"},
                                ],
                            ),
                            className="col-10"
                        ),
                        dbc.Col(
                                dbc.Button("Start", className="custom-btn w-100", id="start-btn", disabled=True),
                                className="col-2"
                            ),
                    ],
                    className="g-3"
                ),
                html.Div(form_fahrmodus1, id="form-param-fahrmodus")   
            ],
            gap=5
        ),
        className="col-9"
      ),
      dbc.Col(
        html.Img(src="/assets/traffic-light-red.svg", height="300px", className="navbar-logo", id="my-traffic-light"),
        className="col-3"
      )
    ],
    className="row-cols-2"
)
