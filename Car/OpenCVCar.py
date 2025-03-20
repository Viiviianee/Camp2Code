from CamCar import CamCar
import time

class Opencvcar(CamCar):
    def __init__(self): 
        super().__init__()

    def drive_with_cam(self):
        print("Start Drive with Cam")
        self.starting_time = time.perf_counter()
        while True:
            self.drive(speed=30, steering_angle=self.mean_angle)

if __name__ == "__main__":
    car = Opencvcar()
    car.stop()