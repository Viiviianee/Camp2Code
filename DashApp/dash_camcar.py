from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from flask import Flask, Response
import cv2
import numpy as np
from pathlib import Path
import sys

project_path = Path(__file__).resolve().parent.parent
sys.path.append(str(project_path))
from Car.cam_car import CamCar


server = Flask(__name__)
camcar = CamCar()
cam = camcar.camera

# Nach Farben suchen / filtern
# Werte von oben durch 2

class Processor():
    def __init__(self):
        self.lower_h = 0
        self.upper_h = 180
        self.lower_s = 0
        self.upper_s = 0
        self.lower_v = 255
        self.upper_v = 255
        self.threshold = 10

        self.img_original = None
        self.gray_img = None
        self.img_hsv = None
        self.img_filtered = None
        self.img_blured = None
        self.img_cannied = None
        self.lines = None
        self.line_img = None

    def set_original_img(self, image):
        self.img_original = image
        return self.img_original

    def display_gray(self):
        self.gray_img = cv2.cvtColor(self.img_original, cv2.COLOR_BGR2GRAY)
        return self.gray_img

    def filter_color(self):
        self.img_hsv = cv2.cvtColor(self.img_original, cv2.COLOR_BGR2HSV)
        array_low = np.array([self.lower_h, self.lower_s, self.lower_v])
        array_high= np.array([self.upper_h, self.upper_s, self.upper_v])
        self.img_filtered = cv2.inRange(self.img_hsv, array_low, array_high)
        return self.img_filtered
    
    def create_blur(self):
        self.img_blured = cv2.medianBlur(self.img_filtered, 7)
        return self.img_blured

    def create_canny(self):
        self.img_cannied = cv2.Canny(self.img_blured, 100, 200)
        return self.img_cannied

    def create_lines(self):
        self.lines = cv2.HoughLinesP(self.img_cannied, 1, np.pi/180, threshold=self.threshold)

    def create_img_with_lines (self):
        try:
            self.create_lines()
            line_img = self.gray_img.copy()
            for line in self.lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(line_img, (x1, y1), (x2, y2), (0, 130, 0), 5)
            self.line_img = line_img
            return self.line_img
        except: 
            pass
        
processor = Processor()

# Hilfsfunktion
def live_stream(cam, processor):
    while True:
        processor.set_original_img(image=cam.get_frame())
        gray = processor.display_gray()
        mask = processor.filter_color()
        blurred = processor.create_blur()
        canny = processor.create_canny()
        lines = processor.create_img_with_lines()
        foo_1 = np.hstack([gray, mask])
        foo_2 = np.hstack([blurred, canny])
        try:
            empty = gray.copy()
            empty [:,:] = 255
            foo_3 = np.hstack([lines, empty])
        except:
            empty = gray.copy()
            empty [:,:] = 255
            foo_3 = np.hstack([gray, empty])
        stacked = np.vstack([foo_1, foo_2, foo_3])
        _, frame_as_jpeg = cv2.imencode(".jpeg", stacked)  # Numpy Array in jpeg
        frame_in_bytes = frame_as_jpeg.tobytes()
        frame_as_string = b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame_in_bytes + b"\r\n\r\n"

        yield frame_as_string  # Return nicht möglich, weil die Funktion sonst verlassen wird und somit die While Schleife

@server.route("/video_stream")
def video_stream():
    return Response(live_stream(cam, processor), mimetype="multipart/x-mixed-replace; boundary=frame",)

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets, server=server)

app.layout = html.Div([html.H1("OpenCV Car"), 
                       html.P("Weiterer Text", id="Wert_Slider_1"),
                       dcc.RangeSlider(id="range-slider-1", min=0, max=180, value=[80, 130]),
                       html.P("Weiterer Text", id="Wert_Slider_2"),
                       dcc.RangeSlider(id="range-slider-2", min=0, max=255, value=[40, 255]),
                       html.P("Weiterer Text", id="Wert_Slider_3"),
                       dcc.RangeSlider(id="range-slider-3", min=0, max=255, value=[40, 255]),
                       html.P("Weiterer Text", id="Wert_Slider_4"),
                       dcc.RangeSlider(id="range-slider-4", min=0, max=100, value=[0, 10]),
                       html.Div(html.Img(src="/video_stream"), style={"height": "100px"})
                       ])

@app.callback(
    Output("Wert_Slider_1", "children"),
    Output("Wert_Slider_2", "children"),
    Output("Wert_Slider_3", "children"),
    Output("Wert_Slider_4", "children"),
    Input("range-slider-1", "value"),
    Input("range-slider-2", "value"),
    Input("range-slider-3", "value"),
    Input("range-slider-4", "value"),
)
def update_values(range_slider_1, range_slider_2, range_slider_3, range_slider_4):  # Parameter definiert über Input von app.callback
    h_low, h_high = range_slider_1
    s_low, s_high = range_slider_2
    v_low, v_high = range_slider_3
    _, threshold = range_slider_4
    processor.lower_h = h_low
    processor.upper_h = h_high
    processor.lower_s = s_low
    processor.upper_s = s_high
    processor.lower_v = v_low
    processor.upper_v = v_high
    processor.threshold = threshold
    print(f"Werte von processor Klasse Parameter h: {processor.lower_h}, {processor.upper_h}")
    print(f"Werte von processor Klasse Parameter s: {processor.lower_s}, {processor.upper_s}")
    print(f"Werte von processor Klasse Parameter v: {processor.lower_v}, {processor.upper_v}")
    print(f"Werte von processor Klasse Parameter threshold: {processor.threshold}")
    return f"Hier der range_slider_1 Wert für Parameter h: {h_low} und {h_high}.",\
           f"Hier der range_slider_2 Wert für Parameter s: {s_low} und {s_high}.",\
           f"Hier der range_slider_3 Wert für Parameter v: {v_low} und {v_high}.",\
           f"Hier der range_slider_4 Wert für Parameter threshold: {threshold}.",\


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=False)  # Debug ist false wegen Kamera