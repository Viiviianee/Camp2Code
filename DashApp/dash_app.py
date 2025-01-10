from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
 
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App Layout

app.layout = html.Div()
 
 
if __name__ == "__main__":

    app.run_server(debug=True, host="0.0.0.0", port=8051)
 