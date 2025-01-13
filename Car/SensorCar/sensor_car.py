import sys
import time
import numpy as np
from pathlib import Path
import json

project_path = Path(__file__).resolve().parent.parent
sys.path.append(str(project_path))

from BaseCar.base_car import BaseCar
from SonicCar.sonic_car import SonicCar
from basisklassen import Ultrasonic
from basisklassen import Infrared


class SensorCar(SonicCar):
    def __init__(self):
        super().__init__()
        path = Path(__file__).parents[1].joinpath("BaseCar", "config.json")
        with open(path, "r") as f:
            data = json.load(f)
            cal_vals = data["cal_vals"]
        self.number_digits = 2
        self.distance = None
        self.val_from_infrared = None
        self.no_line_threshhold = 100
        self.ultrasonic = Ultrasonic()
        self.infrared = Infrared(references=cal_vals)

    def get_val_infrared_analog(self):
        return self.infrared.read_analog()
    
    def get_val_infrared_digital(self):
        return self.infrared.read_digital()
    
    def _test_measure(self, time_delay = 2):
        while True:
            print(self.get_val_infrared_analog())
            print(self.get_val_infrared_digital())
            time.sleep(time_delay)
    
    def fahrmodus5(self, speed):
        self.starting_time = time.perf_counter()
        self.fieldnames.append("ir_val")
        no_line_counter = 0
        while True:
            self.val_from_infrared = self.get_val_infrared_digital()
            if self.val_from_infrared == [1, 1, 1, 1, 1]:
                print("Goal reached - quit")
                self.stop()
                self.result[-1]["ir_val"] = self.val_from_infrared
                break
            elif self.val_from_infrared == [1, 0, 0, 0, 0]:
                self.drive(speed=speed, steering_angle=45)
                self.result[-1]["ir_val"] = self.val_from_infrared
            elif self.val_from_infrared == [1, 1, 0, 0, 0]:
                self.drive(speed=speed, steering_angle=55)
                self.result[-1]["ir_val"] = self.val_from_infrared
            elif self.val_from_infrared == [0, 1, 0, 0, 0]:
                self.drive(speed=speed, steering_angle=65)
                self.result[-1]["ir_val"] = self.val_from_infrared
            elif self.val_from_infrared == [0, 1, 1, 0, 0]:
                self.drive(speed=speed, steering_angle=75)
                self.result[-1]["ir_val"] = self.val_from_infrared

            elif self.val_from_infrared == [0, 0, 1, 0, 0]:
                self.drive(speed=speed, steering_angle=90)
                self.result[-1]["ir_val"] = self.val_from_infrared
            
            elif self.val_from_infrared == [0, 0, 1, 1, 0]:
                self.drive(speed=speed, steering_angle=105)
                self.result[-1]["ir_val"] = self.val_from_infrared
            elif self.val_from_infrared == [0, 0, 0, 1, 0]:
                self.drive(speed=speed, steering_angle=115)
                self.result[-1]["ir_val"] = self.val_from_infrared
            elif self.val_from_infrared == [0, 0, 0, 1, 1]:
                self.drive(speed=speed, steering_angle=125)
                self.result[-1]["ir_val"] = self.val_from_infrared
            elif self.val_from_infrared == [0, 0, 0, 0, 1]:
                self.drive(speed=speed, steering_angle=135)
                self.result[-1]["ir_val"] = self.val_from_infrared
    
            else:
                self.drive(speed=speed, steering_angle=90)
                self.result[-1]["ir_val"] = self.val_from_infrared
        self.logging()
    
    def fahrmodus6(self, speed):
        pass
    
    def fahrmodus7(self, speed):
        pass
        


        



    
def main():
    car = SensorCar()
    car.fahrmodus5(20)
    #car._test_measure()
    #car.drive(50,135)
    #time.sleep(10)
    #car.stop()
    
    

if __name__ == "__main__":
    main()
