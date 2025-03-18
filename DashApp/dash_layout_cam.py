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





# Main content layout
content =html.Div(
            [
                html.H2("Kamera Feed"),
                html.Img(
                    src="/Cam/video_feed",
                    style={"width": "30%", "border": "2px red solid"},
                ),
            ]
        ),