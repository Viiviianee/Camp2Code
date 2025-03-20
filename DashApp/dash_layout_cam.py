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

text1 = html.P(" ", id="Wert_Slider_1")
range1 = c.create_range_div(text1, min=0, max=180, value=[80, 140], id="range-slider-1")
text2 = html.P(" ", id="Wert_Slider_2")
range2 = c.create_range_div(text2, min=0, max=255, value=[40, 255], id="range-slider-2")
text3 = html.P(" ", id="Wert_Slider_3")
range3 = c.create_range_div(text3, min=0, max=255, value=[40, 255], id="range-slider-3")
text4 = html.P(" ", id="Wert_Slider_4")
threshold_slider = c.create_param_div(text4, min=0, max=100, step=5, value=10, id="range-slider-4", disabled=False)


# Main content layout
content = dbc.Stack([
    dbc.Row([
        dbc.Col(
            dbc.Select(
                placeholder="Fahrmodus",
                id="my-select-cam-car",
                options=[
                    {"label": "Fahrmodus OpenCV", "value": "1"},
                    {"label": "Fahrmodus Neuronales Netz", "value": "2"},
                ],
            ),
        ),
        dbc.Col(dbc.Button("Start", className="custom-btn w-100", id="start-btn-cam-car", disabled=False, n_clicks=0)),
        dbc.Col(dbc.Button("Stop", className="custom-btn w-100", id="stop-btn-cam-car", disabled=False, n_clicks=0))
    ]),

    range1,
    range2,
    range3,
    threshold_slider,
    
    dbc.Row([
        dbc.Col(
            c.create_cam_div("Colored - Original", "/Cam/video_feed1")
        ),
        dbc.Col(
            c.create_cam_div("HSV - ROI", "/Cam/video_feed2")
        ),
        dbc.Col(
            c.create_cam_div("Blurred - ROI", "/Cam/video_feed3")
        ),
        dbc.Col(
            c.create_cam_div("Edges - ROI", "/Cam/video_feed4")
        ),
    ]),

])
