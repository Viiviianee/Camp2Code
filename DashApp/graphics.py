from dash import Dash, html, Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv("C:\\Users\\bbern\\Downloads\\log.csv")

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = [
    dbc.CardGroup([
        dbc.Label("Choose an option:", html_for='my_dropdown')
]),
    dbc.Row([
    dbc.Col(dcc.Dropdown(
        id='my_dropdown',
        options=[
            {"label": "Speed", "value" : "speed"},
            {"label": "Steering angle", "value": "steering_angle"},
            {"label": "Direction", "value": "direction"},
            {"label": "Ultrasonicsensor", "value": "distance_ahead"},
        ],
        value="speed")),  # Standardwert
    dbc.Col(dcc.Graph(figure={}, id='my_graph'), xs=12, md=12),
])
    
]

# Add controls to build the interaction
@callback( #calls the connected function (in this case update:graph()) as soon as the Input changes
    Output(component_id='my_graph', component_property='figure'),
    Input(component_id='my_dropdown', component_property='value')
)
def update_graph(value): # the function argument comes from the component property of the Input
    possible_values = {"speed" : "speed [x/y]",
                       "steering_angle" : "steering_angle [°]",
                       "direction" : "direction [-]",
                       "distance_ahead" : "distance to obstacle [cm]"
                       }
    figure=px.line(df, x='time', y=value, labels={"time": "time [s]", value: possible_values[value]}) 
    return figure # the returned object is assigned to the component property of the Output

# Run the app
if __name__ == '__main__':
    app.run(debug=True)