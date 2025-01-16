import sys
import time
import numpy as np
from pathlib import Path
import json
from datetime import datetime

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
        self.no_line_counter = 0
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

    def _drive_and_log(self, speed, steering_angle, flag_previous=False, using_ultrasonic=False):
        self.drive(speed, steering_angle=steering_angle)
        self.result[-1]["ir_val"] = self.val_from_infrared
        if using_ultrasonic:
            self.result[-1]["distance_ahead"] = self.distance
        if flag_previous:
            self.steering_angle_previous = steering_angle
        print(f"time: {datetime.now()}, speed: {speed}, steering_angle: {steering_angle}, ir_value: {self.val_from_infrared} ")

    def _stop_and_log(self, using_ultrasonic=False):
        self.stop()
        self.result[-1]["ir_val"] = self.val_from_infrared
        if using_ultrasonic:
            self.result[-1]["distance_ahead"] = self.distance


    def fahrmodus5(self, speed, driving_back=False, react_to_obstacles=False):
        if "ir_val" not in self.fieldnames:
            self.fieldnames.append("ir_val")
        if react_to_obstacles:
            fail_counter = 0
            if "distance_ahead" not in self.fieldnames:
                self.fieldnames.append("distance_ahead")
        self.starting_time = time.perf_counter()
        while True:
            self.val_from_infrared = self.get_val_infrared_digital()
            if react_to_obstacles:
                self.distance = self.get_distance()
                if self.distance < 20 and self.distance > 0:
                    print("Obstacle detected!")
                    self._stop_and_log(using_ultrasonic=True)
                    self.ultrasonic.stop()
                    break
                elif self.distance < -2:
                    print(f"Sensor error! {fail_counter}")
                    try:
                        self.result[-1]["distance_ahead"] = self.distance
                        self.result[-1]["ir_val"] = self.val_from_infrared
                    except IndexError:
                        pass
                    fail_counter += 1
                    if fail_counter >= 10000:
                        self._stop_and_log(using_ultrasonic=True)
                        self.ultrasonic.stop()
                        break
            if self.val_from_infrared == [1, 1, 1, 1, 1]:
                print("Goal reached - quit")
                if react_to_obstacles:
                    self._stop_and_log(using_ultrasonic=True)
                else:
                    self._stop_and_log(using_ultrasonic=False)
                break

            elif self.val_from_infrared == [1, 0, 0, 0, 0]:
                if driving_back:
                    if react_to_obstacles:
                        while True:
                            self.val_from_infrared = self.get_val_infrared_digital()
                            self._drive_and_log(speed=-35, steering_angle=130, flag_previous=False, using_ultrasonic=True)
                            if self.val_from_infrared == [0, 0, 1, 0, 0]\
                                or self.val_from_infrared == [0, 1, 1, 0, 0]\
                                or self.val_from_infrared == [1, 1, 1, 0, 0]\
                                or self.val_from_infrared == [0, 1, 1, 1, 0]\
                            :
                                self._drive_and_log(speed=35, steering_angle=60, flag_previous=False, using_ultrasonic=True)
                                time.sleep(0.35)
                                break
                    else:
                        while True:
                            self.val_from_infrared = self.get_val_infrared_digital()
                            self._drive_and_log(speed=-35, steering_angle=130, flag_previous=False, using_ultrasonic=False)
                            if self.val_from_infrared == [0, 0, 1, 0, 0]\
                                or self.val_from_infrared == [0, 1, 1, 0, 0]\
                                or self.val_from_infrared == [1, 1, 1, 0, 0]\
                                or self.val_from_infrared == [0, 1, 1, 1, 0]\
                            :
                                self._drive_and_log(speed=35, steering_angle=60, flag_previous=False, using_ultrasonic=False)
                                time.sleep(0.35)
                                break           
                else:
                    self._drive_and_log(speed=speed, steering_angle=45, flag_previous=True)


            elif self.val_from_infrared == [0, 1, 0, 0, 0]:
                if react_to_obstacles:
                    self._drive_and_log(speed=speed, steering_angle=67.5, flag_previous=True, using_ultrasonic=True)
                else:
                    self._drive_and_log(speed=speed, steering_angle=67.5, flag_previous=True, using_ultrasonic=False)
    
            elif self.val_from_infrared == [0, 0, 1, 0, 0]:
                if react_to_obstacles:
                    self._drive_and_log(speed=speed, steering_angle=90, flag_previous=True, using_ultrasonic=True)
                else:
                    self._drive_and_log(speed=speed, steering_angle=90, flag_previous=True, using_ultrasonic=False)

            elif self.val_from_infrared == [0, 0, 0, 1, 0]:
                if react_to_obstacles:
                    self._drive_and_log(speed=speed, steering_angle=112.5, flag_previous=True, using_ultrasonic=True)
                else:
                    self._drive_and_log(speed=speed, steering_angle=112.5, flag_previous=True, using_ultrasonic=False)
            
            elif self.val_from_infrared == [0, 0, 0, 0, 1]:
                if driving_back:
                    if react_to_obstacles:
                        while True:
                            self.val_from_infrared = self.get_val_infrared_digital()
                            self._drive_and_log(speed=-35, steering_angle=50, flag_previous=False, using_ultrasonic=True)
                            if self.val_from_infrared == [0, 0, 1, 0, 0]\
                                or self.val_from_infrared == [0, 0, 1, 1, 0]\
                                or self.val_from_infrared == [0, 0, 1, 1, 1]\
                                or self.val_from_infrared == [0, 1, 1, 1, 0]\
                            :
                                self._drive_and_log(speed=35, steering_angle=120, flag_previous=False, using_ultrasonic=True)
                                time.sleep(0.35)
                                break
                    else:
                        while True:
                            self.val_from_infrared = self.get_val_infrared_digital()
                            self._drive_and_log(speed=-35, steering_angle=50, flag_previous=False, using_ultrasonic=False)
                            if self.val_from_infrared == [0, 0, 1, 0, 0]\
                                or self.val_from_infrared == [0, 0, 1, 1, 0]\
                                or self.val_from_infrared == [0, 0, 1, 1, 1]\
                                or self.val_from_infrared == [0, 1, 1, 1, 0]\
                            :
                                self._drive_and_log(speed=35, steering_angle=120, flag_previous=False, using_ultrasonic=False)
                                time.sleep(0.35)
                                break           
                else:
                    self._drive_and_log(speed=speed, steering_angle=135, flag_previous=True)

                
            elif self.val_from_infrared == [0, 0, 0, 0, 0]:
                self.no_line_counter +=1
                if driving_back and self.no_line_counter >= 30:
                    self.no_line_counter = 0
                    if react_to_obstacles:
                        while True:
                            self.val_from_infrared = self.get_val_infrared_digital()
                            self._drive_and_log(speed=-35, steering_angle=90, flag_previous=False, using_ultrasonic=True)
                            if self.val_from_infrared == [0, 0, 1, 0, 0]\
                                or self.val_from_infrared == [0, 0, 0, 1, 0]\
                                or self.val_from_infrared == [0, 1, 0, 0, 0]\
                                or self.val_from_infrared == [0, 0, 1, 1, 0]\
                                or self.val_from_infrared == [0, 1, 1, 0, 0]\
                                or self.val_from_infrared == [0, 0, 1, 1, 1]\
                                or self.val_from_infrared == [1, 1, 1, 0, 0]\
                                or self.val_from_infrared == [0, 1, 1, 1, 0]\
                                or self.val_from_infrared == [1, 1, 1, 1, 1]\
                                :
                                self._drive_and_log(speed=35, steering_angle=90, flag_previous=False, using_ultrasonic=True)
                                time.sleep(0.3)
                                break

                    else:
                        while True:
                            self.val_from_infrared = self.get_val_infrared_digital()
                            self._drive_and_log(speed=-35, steering_angle=90, flag_previous=False, using_ultrasonic=False)
                            if self.val_from_infrared == [0, 0, 1, 0, 0]\
                                or self.val_from_infrared == [0, 0, 0, 1, 0]\
                                or self.val_from_infrared == [0, 1, 0, 0, 0]\
                                or self.val_from_infrared == [0, 0, 1, 1, 0]\
                                or self.val_from_infrared == [0, 1, 1, 0, 0]\
                                or self.val_from_infrared == [0, 0, 1, 1, 1]\
                                or self.val_from_infrared == [1, 1, 1, 0, 0]\
                                or self.val_from_infrared == [0, 1, 1, 1, 0]\
                                or self.val_from_infrared == [1, 1, 1, 1, 1]\
                                :
                                self._drive_and_log(speed=35, steering_angle=90, flag_previous=False, using_ultrasonic=False)
                                time.sleep(0.3)
                                break
            else:
                if react_to_obstacles:
                    self._drive_and_log(speed=speed, steering_angle=self.steering_angle_previous, flag_previous=True, using_ultrasonic=True)
                else:
                    self._drive_and_log(speed=speed, steering_angle=self.steering_angle_previous, flag_previous=True, using_ultrasonic=False)

        self.logging()

    def fahrmodus6(self, speed):
        self.fahrmodus5(speed=speed, driving_back=True, react_to_obstacles=False)

    def fahrmodus7(self, speed):
        self.fahrmodus5(speed=speed, driving_back=True, react_to_obstacles=True)


def main():
    car = SensorCar()
    car.fahrmodus7(40)
    #car.stop()
    #car.infrared.cali_references()
    #car._test_measure()


if __name__ == "__main__":
    main()
