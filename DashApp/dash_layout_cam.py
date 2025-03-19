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

threshold_slider = c.create_param_div("Slider für Parameter threshold", min=0, max=100, step=5, value=10, id="range-slider-4", disabled=False)
range1 = c.create_range_div("Slider für Parameter h", min=0, max=180, value=[80, 140], id="range-slider-1")
range2 = c.create_range_div("Slider für Parameter s", min=0, max=255, value=[40, 255], id="range-slider-2")
range3 = c.create_range_div("Slider für Parameter v", min=0, max=255, value=[40, 255], id="range-slider-3")

# Main content layout
content = dbc.Stack([
    range1,
    range2,
    range3,
    threshold_slider,
    dbc.Row([
        dbc.Col(
            c.create_cam_div("Title1", "/Cam/video_feed1")
        ),
        dbc.Col(
            c.create_cam_div("Title2", "/Cam/video_feed2")
        ),
        dbc.Col(
            c.create_cam_div("Title3", "/Cam/video_feed3")
        ),
        dbc.Col(
            c.create_cam_div("Title4", "/Cam/video_feed4")
        ),
    ]),

])
