import os.path
import json
import uuid
import sys
import datetime
import numpy as np
from cv2 import imencode, imwrite
import cv2
from pathlib import Path
import matplotlib.pylab as plt
from BaseCar.base_car import BaseCar
from basisklassen_cam import Camera


class CamCar(BaseCar):
    def __init__(self):
        self.cam = Camera()
        self.take_image = False
        super().__init__()  # Initialisiert die Basisklassen

        self.lower_h = 0
        self.upper_h = 180
        self.lower_s = 0
        self.upper_s = 0
        self.lower_v = 255
        self.upper_v = 255
        self.threshold = 10

        self.img_original = np.random.randint(0, 256, (300, 400, 3), dtype=np.uint8)
        self.gray_img = np.random.randint(0, 256, (300, 400, 3), dtype=np.uint8)
        self.img_hsv = np.random.randint(0, 256, (300, 400, 3), dtype=np.uint8)
        self.img_filtered = np.random.randint(0, 256, (300, 400, 3), dtype=np.uint8)
        self.img_blured = np.random.randint(0, 256, (300, 400, 3), dtype=np.uint8)
        self.img_cannied = np.random.randint(0, 256, (300, 400, 3), dtype=np.uint8)
        self.lines = np.random.randint(0, 256, (300, 400, 3), dtype=np.uint8)
        self.line_img = np.random.randint(0, 256, (300, 400, 3), dtype=np.uint8)

    def generate_camera_image(self):
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
            frame = self.cam.get_frame()

            _, x = imencode(".jpeg", frame)
            jpeg = x.tobytes()

            if self.speed > 0 and self.take_image:
                self.save_image(image_id, run_id, frame)
                image_id = image_id + 1

            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + jpeg + b"\r\n\r\n")
    
    def save_image(self, image_id, run_id, frame):
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
            "DRC", run_id, current_time, image_id, self.speed, self.steering_angle
        )
        imwrite(path + filename, frame)
        print(filename)

    def set_original_img(self):
        if self.cam.get_frame() is not None:
            self.img_original = self.cam.get_frame()
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
        return self.lines

    def create_img_with_lines(self):
        try:
            self.create_lines()
            line_img = self.gray_img.copy()
            for line in self.lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(line_img, (x1, y1), (x2, y2), (0, 130, 0), 5)
            self.line_img = line_img
            return self.line_img
        except: 
            empty_img = self.img_original.copy()
            empty_img = empty_img [:,:]
            empty_img [:,:] = 255
            self.line_img = empty_img
            return self.line_img

    def helper_1(self):
        while True:
            self.set_original_img()
            self.display_gray()
            self.filter_color()
            self.create_blur()
            self.create_canny()
            self.create_img_with_lines()

            _, frame_as_jpeg = cv2.imencode(".jpeg", self.img_original)  # Numpy Array in jpeg
            frame_in_bytes = frame_as_jpeg.tobytes()
            frame_as_string_color = b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame_in_bytes + b"\r\n\r\n"
            
            yield frame_as_string_color

    def helper_2(self):
        while True:
            _, frame_as_jpeg = cv2.imencode(".jpeg", self.img_filtered)  # Numpy Array in jpeg
            frame_in_bytes = frame_as_jpeg.tobytes()
            frame_as_string_img_filtered = b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame_in_bytes + b"\r\n\r\n"
            yield frame_as_string_img_filtered
    
    def helper_3(self):
        while True:
            _, frame_as_jpeg = cv2.imencode(".jpeg", self.img_blured)  # Numpy Array in jpeg
            frame_in_bytes = frame_as_jpeg.tobytes()
            frame_as_string_blured = b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame_in_bytes + b"\r\n\r\n"
            yield frame_as_string_blured

    def helper_4(self):
        while True:
            _, frame_as_jpeg = cv2.imencode(".jpeg", self.line_img)  # Numpy Array in jpeg
            frame_in_bytes = frame_as_jpeg.tobytes()
            frame_as_string_line = b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame_in_bytes + b"\r\n\r\n"
            yield frame_as_string_line

def main():
    """
    Hauptfunktion, um ein CamCar-Objekt zu erstellen und die Kamera anzuzeigen.
    """
    car = CamCar()
    #car.generate_camera_image()
    img = car.cam.get_frame()
    print (img.shape)


if __name__ == "__main__":
    main()

