from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
from pathlib import Path
import plotly.express as px
import dash_bootstrap_components as dbc

app = Dash(
         __name__, external_stylesheets=[
             dbc.themes.BOOTSTRAP, 
             "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
            ],
            suppress_callback_exceptions=True 
    )

#Dummy Fahrzeugdaten
speed_min = 0
speed_max = 100
speed_mean = 50
driving_time = 10
driving_distance = 500

# Logdaten einlesen 
def read_log_data():
    log_path = Path(__file__).resolve().parent.parent.joinpath("Car", "log.csv")
    df = pd.read_csv(log_path)
    return df

# Logdaten in Dictionaries umwandeln
def log_data_to_dicts(df):
    return df.to_dict('records')

def create_kpi_card(card_id, card_color, header, value):
    card_class_name = "card-" + card_color
    header_class_name = "card-header-" + card_color

    card_content = [
        dbc.CardHeader(header, class_name=header_class_name),
        dbc.CardBody(
            [
                html.H5(value, id=f"{card_id}-value")
            ],
            className="d-flex justify-content-center align-items-center" 
        ),
    ]

    card = dbc.Card(card_content, className=card_class_name + " h-100", id=card_id)

    return card

#Navbar
navbar = dbc.Navbar(
    dbc.Container(
        [
           html.A(
                html.Img(src="/assets/autonomes-auto.png", height="50px", className="navbar-logo")
            ),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Dashboard", href="#", active=True)),
                    dbc.NavItem(dbc.NavLink("Car", href="#")),
                ],
                navbar=True,
                className="me-auto",  # Links linksbündig
            ),
        ],
        fluid=True  # Container über die volle Breite
    ),
    color="dark",
    dark=True,
)

# App Layout
app.layout = html.Div(
    dbc.Stack(
        [
            navbar,
            dbc.Button("Logdaten einlesen", id="load-log-button", n_clicks=0),
            dbc.Stack(
                [
                
                    dbc.Row(
                        [
                            dbc.Col(create_kpi_card("card-speed-min", "pink", "Geschwindigkeit (Min)", speed_min), className="align-items-stretch"),
                            dbc.Col(create_kpi_card("card-speed-max", "green", "Geschwindigkeit (Max)", speed_max), className="align-items-stretch"),
                            dbc.Col(create_kpi_card("card-speed-mean", "orange", "Geschwindigkeit (Mean)", speed_mean), className="align-items-stretch"),
                            dbc.Col(create_kpi_card("card-driving-distance", "yellow", "Zurückgelegte Strecke", driving_distance), className="align-items-stretch"),
                            dbc.Col(create_kpi_card("card-driving-time", "blue", "Fahrzeit", driving_time), className="align-items-stretch"),
                        ],
                        className="row-cols-5 g-3"
                    ),
                    html.Div(
                        dbc.Stack(
                            [
                                #Placeholder can be deleted or replaced
                                html.Div("Platzhalter DropDown", className="div-place-holder"),
                                #Placeholder can be deleted or replaced
                                html.Div("Platzhalter Graph", className="div-place-holder")
                            ],
                            gap=1
                        ),
                        className= "custom-border"
                    )
                ],
                gap=5,
                className="main-container"
            )
        ]
    )
)

@app.callback(
    [Output("card-speed-min-value", "children"),
     Output("card-speed-max-value", "children"),
     Output("card-speed-mean-value", "children"),
     Output("card-driving-distance-value", "children"),
     Output("card-driving-time-value", "children")],
    [Input("load-log-button", "n_clicks")]
)
def update_log_data(n_clicks):
    if n_clicks > 0:
        log_data_df = read_log_data()
        speed_min_log = round(log_data_df['speed'].min(), 1)
        speed_max_log = round(log_data_df['speed'].max(), 1)
        speed_mean_log = round(log_data_df['speed'].mean(), 1)
        driving_distance_log = round((log_data_df['speed'] * log_data_df['time']).sum(), 1)
        driving_time_log = round(log_data_df['time'].sum(), 1)
        return [html.H5(speed_min_log), html.H5(speed_max_log), html.H5(speed_mean_log), html.H5(driving_distance_log), html.H5(driving_time_log)]
    
    return ["0.0", "0.0", "0.0", "0.0", "0.0"]

if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=8051)
