from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

app = Dash(
         __name__, external_stylesheets=[
             dbc.themes.BOOTSTRAP, 
             "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
            ], 
    )

#Dummy Fahrzeugdaten
speed_min = 0
speed_max = 100
speed_mean = 50
driving_time = 10
driving_distance = 500


#Layout-Components

#Cards
def create_kpi_card(card_id, card_color, header, value):
    card_class_name = "card-" + card_color
    header_class_name = "card-header-" + card_color

    card_content = [
        dbc.CardHeader(header, class_name=header_class_name),
        dbc.CardBody(
            [
                html.H5(value)
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
    dark=True,
    className= "custom-navbar"
)

# App Layout
app.layout = html.Div(
    dbc.Stack(
        [
            navbar,
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

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8051)
