from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
from pathlib import Path
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

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
def create_navbar(logo, tab_names, ids):
    navbar = dbc.Navbar(
        dbc.Container(
            [
            html.A(
                    html.Img(src=logo, height="50px", className="navbar-logo")
                ),
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink(tab_names[0], href=tab_names[0], active=True, id=ids[0])),
                        dbc.NavItem(dbc.NavLink(tab_names[1], href=tab_names[1], active=False, id=ids[1])),
                    ],
                    navbar=True,
                    className="me-auto", 
                ),
            ],
            fluid=True 
        ),
        dark= True,
        className= "custom-navbar"
    )
    return navbar

