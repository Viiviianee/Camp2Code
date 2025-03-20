from CamCar import CamCar
import time

class Opencvcar(CamCar):
    def __init__(self): 
        super().__init__()

    def fahrmodus_cam(self):
        self.running=True
        self.starting_time = time.perf_counter()
        while self.running:
            print(self.mean_angle)
            self.drive(speed = 20, steering_angle=self.mean_angle)
            print("################drive abgeschlossen")
        print("####################while durchlaufen")
if __name__ == "__main__":
    car = Opencvcar()
    car.fahrmodus_cam()