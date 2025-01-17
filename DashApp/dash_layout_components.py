from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
from pathlib import Path
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Gauge
def create_gauge(value, color):
    """
    Creates a gauge chart to display a numerical value.

    Args:
        value (float): The value to be shown on the gauge.
        color (str): Hex color code for the gauge bar (e.g., 'FF5733').

    Returns:
        plotly.graph_objects.Figure: A Plotly figure representing the gauge chart.
    """
    unit = "cm/s"  # Define unit
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={'axis': {'range': [None, 100]}, 'bar': {'color': f"#{color}"}},
        number=dict(
            font=dict(size=20),
            suffix=f" {unit}"  # Add unit
        ),
    ))
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=30),
        font=dict(size=12),
        height=150,
        width=200
    )
    return fig

# Card
def create_kpi_card(card_id, card_color, header, gauge=False):
    """
    Creates a KPI card with an optional gauge chart.

    Args:
        card_id (str): ID for the card, used for future reference.
        card_color (str): Color of the card, linked to CSS classes.
        header (str): Header text for the card.
        gauge (bool): Indicates whether to include a gauge chart in the card.

    Returns:
        dbc.Card: A Dash Bootstrap component representing the KPI card.
    """
    card_class_name = "card-" + card_color
    header_class_name = "card-header-" + card_color
    card_body = html.H1("N/A", id=f"{card_id}-value")
    if gauge:
        card_body = dcc.Graph(
            figure=create_gauge(0.0, card_color),
            id=f"{card_id}-value",
        )
    card_content = [
        dbc.CardHeader(header, className=header_class_name),
        dbc.CardBody(
            [
                card_body
            ],
            className="d-flex justify-content-center align-items-center",
        ),
    ]
    return dbc.Card(card_content, className=card_class_name + " h-100", id=card_id)

# Navbar
def create_navbar(logo, tab_names, ids):
    """
    Creates a navigation bar with a logo and two tabs.

    Args:
        logo (str): Path to the logo image file.
        tab_names (list): List of tab names for navigation.
        ids (list): List of IDs for the tabs.

    Returns:
        dbc.Navbar: A Dash Bootstrap component representing the navbar.
    """
    return dbc.Navbar(
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
        dark=True,
        className="custom-navbar"
    )

# Parameter Slider
def create_param_div(label, id, min, max, step, value, disabled):
    """
    Creates a slider control for adjusting parameters.

    Args:
        label (str): Label for the slider.
        id (str): ID of the slider for reference.
        min (float): Minimum value of the slider.
        max (float): Maximum value of the slider.
        step (float): Step size for slider movement.
        value (float): Initial value of the slider.
        disabled (bool): Indicates whether the slider is disabled.

    Returns:
        html.Div: A div container with a label and slider component.
    """
    return html.Div(
        [
            dbc.Label(label, html_for=id),
            dcc.Slider(min=min, max=max, step=step, value=value, id=id, disabled=disabled)
        ],
        className="mb-3",
    )