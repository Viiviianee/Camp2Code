from CamCar import CamCar
import cv2 as cv

class Opencvcar(CamCar):
    def __init__(self): 
        super().__init__()  # Initialisiert die Basisklassen
        self.img=None

    def get_image(self):   
        self.img = self.cam.get_frame()

car=Opencvcar()
car.get_image()
print(car.img.shape)
# Ändern des Farbraums RGB->HSV
img_hsv = cv.cvtColor(car.img, cv.COLOR_BGR2HSV)

