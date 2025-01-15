from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys

# create path to parent directory
project_path = Path(__file__).resolve().parent.parent
sys.path.append(str(project_path))

# select log file
path = project_path.joinpath("Car", "log.csv")

# create dataframe
df = pd.read_csv(path)

# Dropdown options from log file
options_list = list(df.columns)

# Mapping options from log file to show in dropdown
new_dict = {
    "speed": "Speed",
    "steering_angle": "Steering Angle",
    "direction": "Direction",
    "distance_ahead": "Distance to object",
    "ir_val": "Line detection",
}

dd_options = []
for col in options_list[1:]:
    dd_options.append(new_dict.get(col))
print(dd_options)


# Initialize the app
app = Dash()

# App layout
app.layout = html.Div([
    html.Div(children="Chose an option for car data analysis"),
    html.Hr(),
    dcc.Dropdown(
            id='my_dropdown',
            options=[{"label": new_dict.get(col), "value": col} for col in options_list[1:]],
            value="speed",
        ),
    dcc.Graph(figure={}, id='my_graph')
])

# Add controls to build the interaction
@callback(
    Output(component_id='my_graph', component_property='figure'),
    Input(component_id='my_dropdown', component_property='value'),
)
def update_graph(value, new_dict=new_dict):
    if value:
        print(value, new_dict.get(value))
        figure = px.line(
            df,
            x='time',
            y=value,
            labels={"time": "time [s]", value: new_dict.get(value)}
        )
    else:
        figure = px.line()
    return figure

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
