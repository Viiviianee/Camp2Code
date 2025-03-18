from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_layout_components as c
import sys
from pathlib import Path

project_path = Path(__file__).resolve().parent.parent / 'Car'
sys.path.append(str(project_path))
from basisklassen_cam import Camera
from CamCar import CamCar


#Import aus Vorlage

import os.path
import json
import uuid
import dash
from dash import html, dcc
from dash.dependencies import Output, Input, State
from dash import callback_context
from dash_extensions import Keyboard
from flask import Flask, Response, request
import socket
from cv2 import imencode, imwrite
import datetime 

param1 = c.create_param_div("Parameter 1", min=0, max=100, step=5, value=0, id="param1", disabled=False)
param2 = c.create_param_div("Parameter 2", min=0, max=100, step=5, value=0, id="param2", disabled=False)
param3 = c.create_param_div("Parameter 3", min=0, max=100, step=5, value=0, id="param3", disabled=False)
param4 = c.create_param_div("Parameter 4", min=0, max=100, step=5, value=0, id="param4", disabled=False)

# Main content layout
content = dbc.Stack([
    param1,
    param2,
    param3,
    param4,
    dbc.Row([
        dbc.Col(
            html.Div(
                [
                    html.H5("Kamera Feed 1"),
                    html.Img(
                        src="/Cam/video_feed1",
                        style={"width": "100%", "border": "2px red solid"},
                    ),
                ]
            ),
        ),
        dbc.Col(
            html.Div(
                [
                    html.H5("Kamera Feed 2"),
                    html.Img(
                        src="/Cam/video_feed2",
                        style={"width": "100%", "border": "2px red solid"},
                    ),
                ]
            ),
        ),

        dbc.Col(
            html.Div(
                [
                    html.H5("Kamera Feed 3"),
                    html.Img(
                        src="/Cam/video_feed3",
                        style={"width": "100%", "border": "2px red solid"},
                    ),
                ]
            ),
        ),
        dbc.Col(
            html.Div(
                [
                    html.H5("Kamera Feed 4"),
                    html.Img(
                        src="/Cam/video_feed4",
                        style={"width": "100%", "border": "2px red solid"},
                    ),
                ]
            ),
        )
    ]),


])
