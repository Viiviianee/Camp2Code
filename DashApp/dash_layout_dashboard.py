from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_layout_components as cmpnt

content = dbc.Stack(
                [
                    dbc.Row(
                        [
                            dbc.Col(cmpnt.create_kpi_card("card-speed-min", "e9c46b", "Geschwindigkeit (Min)", True), className="align-items-stretch"),
                            dbc.Col(cmpnt.create_kpi_card("card-speed-max", "e66f51", "Geschwindigkeit (Max)", True), className="align-items-stretch"),
                            dbc.Col(cmpnt.create_kpi_card("card-speed-mean", "f3a261", "Geschwindigkeit (Mean)", True), className="align-items-stretch"),
                            dbc.Col(cmpnt.create_kpi_card("card-driving-distance", "2a9d8e", "Zurückgelegte Strecke"), className="align-items-stretch"),
                            dbc.Col(cmpnt.create_kpi_card("card-driving-time", "264553", "Fahrzeit"), className="align-items-stretch"),
                        ],
                        className="row-cols-5 g-3"
                    ),
                    dbc.Button("Logdaten einlesen", id="load-log-button", n_clicks=0, className="custom-btn"),
                    html.Div(
                        dbc.Stack(
                            [
                                dcc.Dropdown(id='my-dropdown'),
                                dcc.Graph(figure={}, id='my-graph')
                            ],
                            gap=1
                        ),
                        className= "custom-border"
                    )
                ],
                gap=5,
            )