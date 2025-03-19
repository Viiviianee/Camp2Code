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

range1 = c.create_range_div(" ", min=0, max=180, value=[80, 140], id="range-slider-1")
text1 = html.P(" ", id="Wert_Slider_1")
range2 = c.create_range_div(" ", min=0, max=255, value=[40, 255], id="range-slider-2")
text2 = html.P(" ", id="Wert_Slider_2")
range3 = c.create_range_div(" ", min=0, max=255, value=[40, 255], id="range-slider-3")
text3 = html.P(" ", id="Wert_Slider_3")
threshold_slider = c.create_param_div(" ", min=0, max=100, step=5, value=10, id="range-slider-4", disabled=False)
text4 = html.P(" ", id="Wert_Slider_4")



# Main content layout
content = dbc.Stack([
    text1,
    range1,
    text2,
    range2,
    text3,
    range3,
    text4,
    threshold_slider,
    dbc.Row([
        dbc.Col(
            c.create_cam_div("Colored", "/Cam/video_feed1")
        ),
        dbc.Col(
            c.create_cam_div("Filtered", "/Cam/video_feed2")
        ),
        dbc.Col(
            c.create_cam_div("Blurred", "/Cam/video_feed3")
        ),
        dbc.Col(
            c.create_cam_div("Edges", "/Cam/video_feed4")
        ),
    ]),

])
