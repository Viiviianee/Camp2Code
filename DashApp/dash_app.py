from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
 
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#Fahrzeugdaten
speed_min = 0
speed_max = 100
speed_mean = 50
driving_time = 10
driving_distance = 500

def create_kpi_card(card_id, header, value):
    card = dbc.Card(
        [
            dbc.CardHeader(header),
            dbc.CardBody(
                [
                    html.H5(value),
                    dbc.Button("Details", color="primary")
                ]
            ), 
        ],
        id=card_id
    )
    return card

# App Layout
app.layout = html.Div(
    [
        dbc.Row(
                [
                    html.H1(["Dashboard"], id="my-header")
                ]
        ),
        dbc.Row(
            [
                dbc.Col(create_kpi_card("card-speed-min", "Geschwindigkeit (Min)", speed_min), width=2),
                dbc.Col(create_kpi_card("card-speed-max", "Geschwindigkeit (Max)", speed_max), width=2),
                dbc.Col(create_kpi_card("card-speed-mean", "Geschwindigkeit (Mean)", speed_mean), width=2)
            ]
        ),
        dbc.Row(
            [
                dbc.Col(create_kpi_card("card-driving-distance", "Zurückgelegte Strecke", driving_distance ), width=2),
                dbc.Col(create_kpi_card("card-driving-time", "Fahrzeit", driving_time), width=2)
            ]
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8051)