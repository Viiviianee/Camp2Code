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
    
    def _drive_and_log(self, speed, steering_angle):
        self.drive(speed, steering_angle=steering_angle)
        self.result[-1]["ir_val"] = self.val_from_infrared
    
    def _stop_and_log(self):
        self.stop()
        self.result[-1]["ir_val"] = self.val_from_infrared

    def fahrmodus5(self, speed):
        if "ir_val" not in self.fieldnames:
            self.fieldnames.append("ir_val")
        self.starting_time = time.perf_counter()
        no_line_counter = 0
        while True:
            self.val_from_infrared = self.get_val_infrared_digital()
            if self.val_from_infrared == [1, 1, 1, 1, 1]:
                print("Goal reached - quit")
                self._stop_and_log()
                break
            elif self.val_from_infrared == [1, 0, 0, 0, 0]:
                self._drive_and_log(speed=speed, steering_angle=45)
            elif self.val_from_infrared == [1, 1, 0, 0, 0]:
                self._drive_and_log(speed=speed, steering_angle=55)
            elif self.val_from_infrared == [0, 1, 0, 0, 0]:
                self._drive_and_log(speed=speed, steering_angle=65)
            elif self.val_from_infrared == [0, 1, 1, 0, 0]:
                self._drive_and_log(speed=speed, steering_angle=75)

            elif self.val_from_infrared == [0, 0, 1, 0, 0] or self.val_from_infrared == [0, 0, 0, 0, 0]:
                self._drive_and_log(speed=speed, steering_angle=90)
            
            elif self.val_from_infrared == [0, 0, 1, 1, 0]:
                self._drive_and_log(speed=speed, steering_angle=105)
            elif self.val_from_infrared == [0, 0, 0, 1, 0]:
                self._drive_and_log(speed=speed, steering_angle=115)
            elif self.val_from_infrared == [0, 0, 0, 1, 1]:
                self._drive_and_log(speed=speed, steering_angle=125)
            elif self.val_from_infrared == [0, 0, 0, 0, 1]:
                self._drive_and_log(speed=speed, steering_angle=135)

            else:
                continue
        self.logging()
    
    def fahrmodus6(self, speed):
        pass
    
    def fahrmodus7(self, speed):
        pass
        

def main():
    car = SensorCar()
    car.fahrmodus5(20)
    #car.stop()
    #car.infrared.cali_references()
    #car._test_measure()

if __name__ == "__main__":
    main()
