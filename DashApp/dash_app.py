from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
from pathlib import Path
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

app = Dash(
         __name__, external_stylesheets=[
             dbc.themes.BOOTSTRAP, 
             "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
            ],
            suppress_callback_exceptions=True 
    )

# Logdaten einlesen 
def read_log_data():
    log_path = Path(__file__).resolve().parent.parent.joinpath("Car", "log.csv")
    df = pd.read_csv(log_path)
    return df

# Logdaten in Dictionaries umwandeln
def log_data_to_dicts(df):
    return df.to_dict('records')

# Layout Components

# Gauge
def create_gauge(value, color):
    unit = "m/s"  # Einheit definieren
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={'axis': {'range': [None, 100]}, 'bar': {'color': f"#{color}" }},
        number=dict(
            font=dict(size=20),
            suffix=f" {unit}"  # Einheit hinzufügen
        ),
    ))
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=30),
        font=dict(size=12),
        height=150,
        width=200
    )
    return fig

#Card
def create_kpi_card(card_id, card_color, header, gauge=False):
    card_class_name = "card-" + card_color
    header_class_name = "card-header-" + card_color
    card_body = html.H1(0.0, id=f"{card_id}-value")
    if  gauge == True:
        card_body = dcc.Graph(
                    figure=create_gauge(0.0, card_color),
                    id=f"{card_id}-value",
                )
    card_content = [
        dbc.CardHeader(header, class_name=header_class_name),
        dbc.CardBody(
            [
                card_body
            ],
            className="d-flex justify-content-center align-items-center",
        ),
    ]

    card = dbc.Card(card_content, className=card_class_name + " h-100", id=card_id)
    return card
  
#Navbar
navbar = dbc.Navbar(
    dbc.Container(
        [
           html.A(
                html.Img(src="/assets/car.svg", height="50px", className="navbar-logo")
            ),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Dashboard", href="Dashboard", active=True, id="nav-dashboard")),
                    dbc.NavItem(dbc.NavLink("Car", href="Car", active=False, id="nav-car")),
                ],
                navbar=True,
                className="me-auto",  # Links linksbündig
            ),
        ],
        fluid=True 
    ),
    dark= True,
    className= "custom-navbar"
)

# App Layout
app.layout = html.Div(
    dbc.Stack(
        [
            navbar,
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content', className="main-container"),  
        ]
    )
)

@app.callback(
    [Output('nav-dashboard', 'active'), Output('nav-car', 'active')],
    [Input('url', 'pathname')]
)

def update_navbar_active(pathname):
    # Setze den active-Status basierend auf der URL
    return pathname == '/', pathname == '/Car'

# Callback für das Laden des richtigen Inhalts basierend auf der URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]  # Input ist die aktuelle URL
)

def display_page(pathname):
    if pathname is None or pathname == '/' or pathname =='/Dashboard':
        content = dbc.Stack(
                [
                    dbc.Row(
                        [
                            dbc.Col(create_kpi_card("card-speed-min", "e9c46b", "Geschwindigkeit (Min)", True), className="align-items-stretch"),
                            dbc.Col(create_kpi_card("card-speed-max", "e66f51", "Geschwindigkeit (Max)", True), className="align-items-stretch"),
                            dbc.Col(create_kpi_card("card-speed-mean", "f3a261", "Geschwindigkeit (Mean)", True), className="align-items-stretch"),
                            dbc.Col(create_kpi_card("card-driving-distance", "2a9d8e", "Zurückgelegte Strecke"), className="align-items-stretch"),
                            dbc.Col(create_kpi_card("card-driving-time", "264553", "Fahrzeit"), className="align-items-stretch"),
                        ],
                        className="row-cols-5 g-3"
                    ),
                    dbc.Button("Logdaten einlesen", id="load-log-button", n_clicks=0, className="custom-btn"),
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
            )
        return content
    elif pathname == '/Car':
        content = dbc.Stack(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Select(
                            placeholder="Fahrmodus",
                            id="select",
                            options=[
                                {"label": "Fahrmodus 1", "value": "1"},
                                {"label": "Fahrmodus 2", "value": "2"},
                                {"label": "Fahrmodus 3", "value": "3"},
                                {"label": "Fahrmodus 4", "value": "4"},
                                {"label": "Fahrmodus 5", "value": "5"},
                                {"label": "Fahrmodus 6", "value": "6"},
                            ],
                        )
                    ),
                    dbc.Col(
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.H6("Anzahl der Runden:"),
                                    className="d-flex justify-content-end align-items-center"
                                ),
                                dbc.Col(
                                    html.Div(
                                            dbc.Input(type="number", min=1, max=10, step=1),
                                            id="styled-numeric-input",
                                            className="d-flex justify-content-center align-items-center"
                                    ),  
                                ) 
                            ]
                           
                        )
                            
                        ),
                ],
                className="row-cols-3 g-3"
            )    
        )
        return content

@app.callback(
    [Output("card-speed-min-value", "figure"),
     Output("card-speed-max-value", "figure"),
     Output("card-speed-mean-value", "figure"),
     Output("card-driving-distance-value", "children"),
     Output("card-driving-time-value", "children")],
    [Input("load-log-button", "n_clicks")]
)
def update_log_data(n_clicks):
    if n_clicks > 0:
        log_data_df = read_log_data()

        speeds_greater_than_zero = log_data_df['speed'][log_data_df['speed'] > 0]
        if not speeds_greater_than_zero.empty:
            speed_min_log = round(speeds_greater_than_zero.min(), 1)
        else:
            speed_min_log = 0.0

        speed_max_log = round(log_data_df['speed'].max(), 1)
        speed_mean_log = round(log_data_df['speed'].mean(), 1)
        driving_distance_log = round((log_data_df['speed'] * log_data_df['time']).sum(), 1)
        driving_time_log = round(log_data_df.iloc[-1]['time'] - log_data_df.iloc[0]['time'], 1)

        return [
                create_gauge(speed_min_log, "e9c46b"),
                create_gauge(speed_max_log, "e66f51"), 
                create_gauge(speed_mean_log, "f3a261"), 
                html.H5(driving_distance_log),
                html.H5(driving_time_log)
            ]
    
    return [create_gauge(0.0, "e9c46b"), create_gauge(0.0, "e66f51"), create_gauge(0.0, "f3a261"), "0.0", "0.0"]

   
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=8051)
