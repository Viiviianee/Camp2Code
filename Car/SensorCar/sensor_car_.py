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
        self.steering_angle_previous = 90
        self.flag_started = 0

    def get_val_infrared_analog(self):
        return self.infrared.read_analog()

    def get_val_infrared_digital(self):
        return self.infrared.read_digital()

    def _test_measure(self, time_delay=2):
        while True:
            print(self.get_val_infrared_analog())
            print(self.get_val_infrared_digital())
            time.sleep(time_delay)

    def _drive_and_log(self, speed, steering_angle, flag_previous=False):
        self.drive(speed, steering_angle=steering_angle)
        self.result[-1]["ir_val"] = self.val_from_infrared
        if flag_previous:
            self.steering_angle_previous = steering_angle

    def _stop_and_log(self):
        self.stop()
        self.result[-1]["ir_val"] = self.val_from_infrared


    def fahrmodus5(self, speed, driving_back=False):
        if "ir_val" not in self.fieldnames:
            self.fieldnames.append("ir_val")
        self.starting_time = time.perf_counter()
        while True:
            self.val_from_infrared = self.get_val_infrared_digital()
            if self.val_from_infrared == [1, 1, 1, 1, 1]:
                print("Goal reached - quit")
                self._stop_and_log()
                break
            elif self.val_from_infrared == [1, 0, 0, 0, 0] \
                or self.val_from_infrared == [1, 1, 0, 0, 0]:
                if driving_back:
                    self._drive_and_log(speed=-30, steering_angle=130, flag_previous=False) # -30, 130
                    time.sleep(0.35) # 0.35
                    self._drive_and_log(speed=speed, steering_angle=90, flag_previous=False)
                    time.sleep(0.35) # 0.35
                else:
                    self._drive_and_log(speed=speed, steering_angle=45, flag_previous=True)
            elif self.val_from_infrared == [0, 1, 0, 0, 0]:
                self._drive_and_log(speed=speed, steering_angle=67.5, flag_previous=True)

            elif self.val_from_infrared == [0, 0, 1, 0, 0]:
                self._drive_and_log(speed=speed, steering_angle=90, flag_previous=True)

            elif self.val_from_infrared == [0, 0, 0, 1, 0]:
                self._drive_and_log(speed=speed, steering_angle=112.5, flag_previous=True)
            elif self.val_from_infrared == [0, 0, 0, 0, 1]\
                    or self.val_from_infrared == [0, 0, 0, 1, 1]:
                if driving_back:
                    self._drive_and_log(speed=-30, steering_angle=50, flag_previous=False) # -30, 50
                    time.sleep(0.35) # 0.35
                    self._drive_and_log(speed=speed, steering_angle=90, flag_previous=False)
                    time.sleep(0.35) # 0.35

            else:
                self._drive_and_log(speed=speed, steering_angle=self.steering_angle_previous)
        self.logging()

    def fahrmodus6(self, speed):
        self.fahrmodus5(speed=speed, driving_back=True)

    def fahrmodus7(self, speed):
        pass


def main():
    car = SensorCar()
    car.fahrmodus6(30)
    #car.stop()
    #car.infrared.cali_references()
    #car._test_measure()


if __name__ == "__main__":
    main()
