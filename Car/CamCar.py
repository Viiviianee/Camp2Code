import os.path
import json
import uuid
import sys
import datetime
import numpy as np
from cv2 import imencode, imwrite
from pathlib import Path
import matplotlib.pylab as plt
from BaseCar.base_car import BaseCar
from basisklassen_cam import Camera


class CamCar(BaseCar):
    def __init__(self):
        self.cam = Camera()
        self.take_image = False
        super().__init__()  # Initialisiert die Basisklassen

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


def main():
    """
    Hauptfunktion, um ein CamCar-Objekt zu erstellen und die Kamera anzuzeigen.
    """
    car = CamCar()
    car.generate_camera_image()


if __name__ == "__main__":
    main()

