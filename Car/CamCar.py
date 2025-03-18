import sys
import time
import json
import numpy as np
import cv2
from pathlib import Path
import matplotlib.pylab as plt
from BaseCar.base_car import BaseCar
from basisklassen_cam import Camera


project_path = Path(__file__).resolve().parent.parent
sys.path.append(str(project_path))


class CamCar(BaseCar):
    def __init__(self):
        self.cam = Camera()
        super().__init__()  # Initialisiert die Basisklassen

    def show_camera_feed(self):
        """
        Funktion, um den Kamerastream anzuzeigen.
        """
        # Kamera initialisieren
        

        try:
            # Einzelnes Bild abrufen
            frame = self.cam.get_frame()

            # Bild anzeigen
            cv2.imshow("Kamera-Bild", frame)

            # Warten, bis eine Taste gedrückt wird
            cv2.waitKey(0)
        finally:
            # Ressourcen freigeben
            self.cam.release()
            cv2.destroyAllWindows()


def main():
    """
    Hauptfunktion, um ein CamCar-Objekt zu erstellen und die Kamera anzuzeigen.
    """
    car = CamCar()
    car.show_camera_feed()


if __name__ == "__main__":
    main()

