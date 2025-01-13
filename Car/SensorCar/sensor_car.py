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
            self.drive(speed)
            self.val_from_infrared = self.get_val_infrared_digital()
            self.result[-1]["ir_val"] = self.val_from_infrared
            # if self.val_from_infrared == [0, 0, 0, 0, 0]:
            #     no_line_counter += 1
            #     if no_line_counter >= self.no_line_threshhold:
            #         print("No line - quit")
            #         break
            if self.val_from_infrared == [1, 1, 1, 1, 1]:
                print("Goal reached - quit")
                self.stop()
                self.result[-1]["ir_val"] = self.val_from_infrared
                break
        self.logging()
        


        



    
def main():
    car = SensorCar()
    car.fahrmodus5(30)
    
    

if __name__ == "__main__":
    main()
