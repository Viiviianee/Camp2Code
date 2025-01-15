from dash import html
import dash_bootstrap_components as dbc

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