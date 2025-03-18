from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_layout_components as c
import sys
from pathlib import Path

project_path = Path(__file__).resolve().parent.parent / 'Car'
sys.path.append(str(project_path))
from basisklassen_cam import Camera
from BaseCar.base_car import BaseCar


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
from datetime import datetime




car = BaseCar()
take_image = False


def generate_camera_image(camera_class):
    """Generator for the images from the camera for the live view in dash

    Args:
        camera_class (object): Object of the class Camera

    Yields:
        bytes: Bytes string with the image information
    """
    image_id = 0
    run_id = str(uuid.uuid4())[:8]
    if not os.path.exists(os.path.join(os.getcwd(), "images")):
        os.makedirs(os.path.join(os.getcwd(), "images"))
    while True:
        frame = camera_class.get_frame()

        _, x = imencode(".jpeg", frame)
        jpeg = x.tobytes()

        if car.speed > 0 and take_image:
            save_image(image_id, run_id, frame)
            image_id = image_id + 1

        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + jpeg + b"\r\n\r\n")


def save_image(image_id, run_id, frame):
    """Save an image from the camera

    Args:
        camera_class: Object of the class Camera
        image_id: Integer with the image id
        run_id: String with the run id
        frame: Frame from the camera
    """
    current_time = datetime.now().strftime("%Y%m%d_%H-%M-%S")
    path = "./images/"
    filename = "IMG_{}_{}_{}_{:04d}_S{:03d}_A{:03d}.jpg".format(
        "DRC", run_id, current_time, image_id, car.speed, car.steering_angle
    )
    imwrite(path + filename, frame)
    print(filename)


server = Flask(__name__)
app = dash.Dash(__name__, server=server)


def shutdown_server():
    """Will shut down the server when the function is called

    Raises:
        RuntimeError: If the server runtime is not corret
    """
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@server.route("/video_feed")
def video_feed():
    """Will return the video feed from the camera

    Returns:
        Response: Response object with the video feed
    """
    return Response(
        generate_camera_image(Camera()),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )

# Ende Import aus Vorlage 



# Main content layout
content =html.Div(
            [
                html.H2("Kamera Feed"),
                html.Img(
                    src="/video_feed",
                    style={"width": "30%", "border": "2px black solid"},
                ),
            ]
        ),