from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

from pathlib import Path
import csv
import plotly.graph_objects as go


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def create_kpi_card(card_id, header, value):
    card = dbc.Card([dbc.CardHeader(header), dbc.CardBody([html.H5(value)])],id=card_id
    )
    return card

# App Layout

class Datahandler:
    def __init__(self):
        self.log_values = None
        self.path = Path(__file__).parents[1].joinpath("Car/log.csv")
        self.keys = None


    def read_data_log(self):
        path = self.path
        with open(path, "r", encoding="unicode_escape") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            dictionaries = [dict(d) for d in reader]
            values  = {}
            for fieldname in fieldnames:
                try:
                    values[fieldname] = [float(dictionary[fieldname]) for dictionary in dictionaries]
                except ValueError as _:
                    print("Casting to float not possible")
                    continue
            self.log_values = values
            self.keys = fieldnames
            self.keys = [fieldname for fieldname in fieldnames if fieldname != "time"]

    def plot_values(self):
        keys = list(self.log_values.keys())
        for key in keys:
            if key == "time":
                continue
            x = self.log_values["time"]
            y = self.log_values[key]
            fig = go.Figure(data=go.Scatter(x=x, y=y, mode="markers", name="Scatterplot"))
            fig.update_layout(title=f"{key} over time", xaxis_title="time", yaxis_title=key)
            fig.add_trace(go.Line(x=x, y=y, name="Lineplot"))
            fig.show()


app.layout = html.Div(
    [
        dbc.Row(
                [
                    html.H1(children=["Dash-APP for PiCar"], id="header"),
                    html.Hr()
                ]
        ),


        dbc.Row(
                [dbc.Col(dbc.Card(
                        [
                        dbc.CardBody([dbc.Button("Read_Data", color="secondary", n_clicks=0, id="load_button")])
                        ]
                        ), width = 0.5
                        ),
                dbc.Col(dbc.Alert("", color="light", id = "information_box"), width = 11
                        )
                ]
                ),


        dbc.Row(
            [
                dbc.Col(create_kpi_card("card-speed-min", "Geschwindigkeit (Min)", 0), width=4),
                dbc.Col(create_kpi_card("card-speed-max", "Geschwindigkeit (Max)", 0), width=4),
                dbc.Col(create_kpi_card("card-speed-mean", "Geschwindigkeit (Mean)", 0), width=4)
            ]
        ),
        dbc.Row(
            [
                dbc.Col(create_kpi_card("card-driving-distance", "Zurückgelegte Strecke", 0 ), width=4),
                dbc.Col(create_kpi_card("card-driving-time", "Fahrzeit", 0), width=4)
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Dropdown(options=[], value = None, id="dropdown_1"), width=4),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="my_graph_1"), width=8),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Dropdown(options=[], value = None, id="dropdown_2"), width=4),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="my_graph_2"), width=8),
            ]
        ),
    ]
)

@app.callback(Output("dropdown_1", "options"), Input("load_button", "n_clicks"), prevent_initial_call=True)
def read_data_dropdown_1(n_clicks):
    datahandler = Datahandler()
    datahandler.read_data_log()
    return datahandler.keys

@app.callback(Output("dropdown_2", "options"), Input("load_button", "n_clicks"), prevent_initial_call=True)
def read_data_dropdown_2(n_clicks):
    datahandler = Datahandler()
    datahandler.read_data_log()
    return datahandler.keys

@app.callback(Output("information_box", "children"), Input("load_button", "n_clicks"), prevent_initial_call=True)
def update_information_box_text(n_clicks):
    try:
        datahandler = Datahandler()
        datahandler.read_data_log()
        return "Loading was successful"
    except Exception as _:
        return "Loading was not successful"


@app.callback(Output("information_box", "color"), Input("load_button", "n_clicks"), prevent_initial_call=True)
def update_information_box_color(n_clicks):
    try:
        datahandler = Datahandler()
        datahandler.read_data_log()
        return "success"
    except Exception as _:
        return "danger"

@app.callback(Output("card-speed-min", "children"), Input("load_button", "n_clicks"), prevent_initial_call=True)
def update_card_speed_min(n_clicks):
    datahandler = Datahandler()
    datahandler.read_data_log()
    min_val = min(datahandler.log_values['speed'])
    return [dbc.CardHeader("Geschwindigkeit (Min)"), dbc.CardBody([html.H5(min_val)])]

@app.callback(Output("card-speed-max", "children"), Input("load_button", "n_clicks"), prevent_initial_call=True)
def update_card_speed_max(n_clicks):
    datahandler = Datahandler()
    datahandler.read_data_log()
    max_val = max(datahandler.log_values["speed"])
    return [dbc.CardHeader("Geschwindigkeit (Min)"), dbc.CardBody([html.H5(max_val)])]

@app.callback(Output("card-speed-mean", "children"), Input("load_button", "n_clicks"), prevent_initial_call=True)
def update_card_speed_average(n_clicks):
    datahandler = Datahandler()
    datahandler.read_data_log()
    average = sum(datahandler.log_values["speed"]) / len(datahandler.log_values["speed"])
    return [dbc.CardHeader("Geschwindigkeit (Min)"), dbc.CardBody([html.H5(average)])]

@app.callback(Output("card-driving-distance", "children"), Input("load_button", "n_clicks"), prevent_initial_call=True)
def update_card_distance(n_clicks):
    datahandler = Datahandler()
    datahandler.read_data_log()
    distance = sum(datahandler.log_values["speed"]) / len(datahandler.log_values["speed"]) * datahandler.log_values["time"][-1]
    return [dbc.CardHeader("Geschwindigkeit (Min)"), dbc.CardBody([html.H5(distance)])]

@app.callback(Output("card-driving-time", "children"), Input("load_button", "n_clicks"), prevent_initial_call=True)
def update_card_driving_time(n_clicks):
    datahandler = Datahandler()
    datahandler.read_data_log()
    time = datahandler.log_values["time"][-1]
    return [dbc.CardHeader("Geschwindigkeit (Min)"), dbc.CardBody([html.H5(time)])]


@app.callback(Output("my_graph_1", "figure"),
            Input("dropdown_1", "value"), prevent_initial_call=True)
def update_plot_1(dd_value):
    datahandler = Datahandler()
    datahandler.read_data_log()
    x = datahandler.log_values["time"]
    y = datahandler.log_values[dd_value]
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode="markers", name="Scatterplot"))
    fig.update_layout(title=f"{dd_value} over time", xaxis_title="time", yaxis_title=dd_value)
    fig.add_trace(go.Line(x=x, y=y, name="Lineplot"))
    return fig

@app.callback(Output("my_graph_2", "figure"),
            Input("dropdown_2", "value"), prevent_initial_call=True)
def update_plot_2(dd_value):
    datahandler = Datahandler()
    datahandler.read_data_log()
    x = datahandler.log_values["time"]
    y = datahandler.log_values[dd_value]
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode="markers", name="Scatterplot"))
    fig.update_layout(title=f"{dd_value} over time", xaxis_title="time", yaxis_title=dd_value)
    fig.add_trace(go.Line(x=x, y=y, name="Lineplot"))
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
