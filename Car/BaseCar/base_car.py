import click
import time
import numpy as np
import math
import RPi.GPIO as GPIO
import smbus
import json
import csv
import sys
from datetime import datetime
from datetime import timezone
from pathlib import Path

# Pfad relativ zu dieser Datei dynamisch ermitteln
project_path = Path(__file__).resolve().parent.parent
sys.path.append(str(project_path))


from basisklassen import FrontWheels
from basisklassen import BackWheels


class BaseCar:
    """
    A class to represent a basecar.

    Attributes:
    steering angle (int) : Steering angle of the car.
    speed (int) : Speed of the car.
    direction (int) : 0 for stop, 1 for forwards, -1 for backwards.

    """
    def __init__(self):
        """
    Initialize a car object.
    """
        self._steering_angle = 90
        self._speed = 0
        self._direction = 0
        self.result = []
        self.result_t = {}
        self.fieldnames = ["time", "speed", "steering_angle", "direction"]
        self.starting_time = None
        self.number_digits = 1
        path = Path(__file__).parents[0].joinpath("config.json")
        with open(path, "r") as f:
                data = json.load(f)
                turning_offset = data["turning_offset"]
                forward_A = data["forward_A"]
                forward_B = data["forward_B"]
        self.frontwheels = FrontWheels(turning_offset=turning_offset)
        self.backwheels = BackWheels(forward_A = forward_A, forward_B = forward_B )
        self.lst= [
            {"speed" : 30, "steering_angle" : 90, "time" : 3, "stop" : 1},
            {"speed" : -30, "steering_angle" : 90, "time" : 3, "stop" : 1},
            {"speed" : 30, "steering_angle" : 90, "time" : 1, "stop" : 0},
            {"speed" : 30, "steering_angle" : 135, "time" : 8, "stop" : 1},
            {"speed" : -30, "steering_angle" : 135, "time" : 8, "stop" : 0},
            {"speed" : -30, "steering_angle" : 90, "time" : 1, "stop" : 1},
            {"speed" : 30, "steering_angle" : 90, "time" : 1, "stop" : 0},
            {"speed" : 30, "steering_angle" : 45, "time" : 8, "stop" : 1},
            {"speed" : -30, "steering_angle" : 45, "time" : 8, "stop" : 0},
            {"speed" : -30, "steering_angle" : 90, "time" : 1, "stop" : 1}
            ]


    @property
    def steering_angle(self):
        """
        Gets the current steering angle.

        This property retrieves the value of the private `_steering_angle` attribute,
        which represents the angle of the steering mechanism in degrees.

        Returns:
        int: The current steering angle.
        """
        return self._steering_angle

    @steering_angle.setter
    def steering_angle(self,value):
        """
        Sets the steering angle, ensuring it remains within valid bounds.

        This property sets the value of the private `_steering_angle` attribute.
        The angle is clamped to a minimum of 45 degrees and a maximum of 135 degrees.

        Args:
            value (int): The desired steering angle.

        Side Effects:
            If the input value is less than 45, `_steering_angle` is set to 45.
            If the input value is greater than 135, `_steering_angle` is set to 135.
        """
        self._steering_angle=value
        if value < 45:
            self._steering_angle = 45
        if value > 135:
            self._steering_angle = 135


    @property
    def speed(self):
        """Gets the speed. -100-100. 0 is stop. 100 is max speed.
        Returns:
            int: speed of the motors.
        """
        return self._speed

    @speed.setter
    def speed(self,value):
        """Sets the speed. -100-100. 0 is stop. 100 is max speed.
            Args:
                speed (int): speed of the motors.
        """
        self._speed=value
        if value < -100:
            self._speed = -100
        if value > 100:
            self._speed = 100

    @property
    def direction(self):
        """Retruns the current direction of the car.
        Returns:
            int: direction of the car.
        """
        return self._direction

    def drive(self, speed = None, steering_angle = None):
        """This method enables the car to drive at a certain speed and angle depending on the value of the arguments.
            Depending on the positive or negative speed, the direction of travel is set using the 'backwheels.forward()'
            or 'backwheels.backward()' method. A negative speed will set 'directions' to -1. A posotive speed will set 'directions' to 1.

        Args:
            speed (int): speed of the motors. Min is -100. Max is 100. Default to None.
            steering_angle (int): angle of the fron wheels. Min 45 for left turn. Max 135 for right turn. Default to None.
        """
        if speed != None:
            self._speed = speed
        if steering_angle != None:
            self._steering_angle = steering_angle
        self.frontwheels.turn(self._steering_angle)
        self.backwheels.speed = abs(self.speed)
        if self._speed < 0:
            self.backwheels.backward()
            self._direction = -1
        else:
            self.backwheels.forward()
            self._direction = 1
        self.result_t = {
                        "time": round(time.perf_counter() - self.starting_time,self.number_digits),
                        "speed": self.backwheels.speed,
                        "steering_angle": self.steering_angle,
                        "direction": self.direction,
                        }
        self.result.append(self.result_t)


    def stop(self):
        """
        Stop the car.

        This method stops the car by calling the `stop` method on the `backwheels` object and sets the direction to 0.
        """
        self.backwheels.stop()
        self._direction = 0
        self.result_t = {
                        "time": round(time.perf_counter() - self.starting_time,self.number_digits ),
                        "speed": self.backwheels.speed,
                        "steering_angle": self.steering_angle,
                        "direction": self.direction,
                        }
        self.result.append(self.result_t)

    def fahrmodus1(self, speed, time_fw = 3, time_bw = 3, time_sp = 1):
        """Car drives "fahrmodus1": 3sek forwards, 1 sek stop, 3 sek backwards.

            Args:
                speed (int): speed of the motors. Min is -100. Max is 100.
                time_fw (int): duration car drives forward. Default to 3.
                time_bw (int): duration car drives backward. Default to 3.
                time_sp (int): duration car stopps. Default to 1.
        """
        print(f"Start Fahrmodus 1 mit time_fw {time_fw}, time_bw {time_bw} und time_stop {time_sp}")
        self.starting_time = time.perf_counter()

        #fahrt forwärts für 3 sek
        self.drive(speed, 90)
        time.sleep(time_fw)
        self.stop()
        time.sleep(time_sp)
        #fahrt rückwärts für 3 sek
        speed = speed * (-1)
        self.drive(speed)
        time.sleep(time_bw)
        self.stop()
        self.logging()
        print("Ende Fahrmodus 1")


    # def fahrmodus2(self, speed, time_fw=1, time_cw=8, time_ccw=8, time_bw=1):
    #     """Car drives "fahrmodus2": 1sek forwards no steering angle, 8 sek with max steering angle clockwise, 8 sek backwards with max steering angle, 1 sek backwards.
    #                                 1sek forwards no steering angle, 8 sek with max steering angle counterclockwise, 8 sek backwards with max steering angle, 1 sek backwards.
    #         Args:
    #             speed (int): speed of the motors. Min is -100. Max is 100.
    #             time_fw (int): duration car drives forward. Default to 1.
    #             time_bw (int): duration car drives backward. Default to 1.
    #             time_cw (int): duration car cw. Default to 8.
    #             time_ccw (int): duration car ccw. Default to 8.
    #         """
    #     self.drive(speed, 90)
    #     time.sleep(time_fw)
    #     self.drive(steering_angle=135)
    #     time.sleep(time_cw)
    #     self.stop()
    #     speed = speed * (-1)
    #     self.drive(speed)
    #     time.sleep(time_cw)
    #     self.drive(speed, 90)
    #     time.sleep(time_bw)
    #     self.stop()
    #     speed = speed * (-1)
    #     self.drive(speed, 90)
    #     time.sleep(time_fw)
    #     self.drive(steering_angle=45)
    #     time.sleep(time_ccw)
    #     self.stop()
    #     speed = speed * (-1)
    #     self.drive(speed)
    #     time.sleep(time_ccw)
    #     self.drive(speed, 90)
    #     time.sleep(time_bw)
    #     self.stop()
    #     self.logging()

    def fahrmodus1_2(self, mode=0, lst=None):
        """
        Executes the driving mode by processing a list of driving commands.

        Parameters:
        - mode (int): The mode that defines which subset of driving commands to use.
                      - 0 (default) uses the full list (self.lst).
                      - 1 uses the first two elements of self.lst (Fahrmodus1).
                      - 2 uses elements starting from the third element of self.lst (Fahrmodus2).
        - lst (list of dicts, optional): A list of dictionaries containing driving instructions.
                                         If None, uses self.lst.

        Each element in the list should be a dictionary containing the following keys:
        - "speed" (float): The speed at which to drive.
        - "steering_angle" (float): The steering angle to use.
        - "time" (float): The time duration for which to drive at the specified speed and steering angle.

        The method drives the vehicle according to the instructions, and then stops it. After that, it logs the results.
        """
        self.starting_time = time.perf_counter()
        if lst == None:
            lst = self.lst
            if mode == 1:
                lst = self.lst[:2]
            elif mode == 2:
                lst = self.lst[2:]
            elif mode == 0:
                pass
            else:
                print("Value of mode is not valid")
                quit()
        for element in lst:
            self.drive(element["speed"], element["steering_angle"])
            time.sleep(element["time"])
            # if element["stop"] != 0:
            #     print("STOPPED!")
            #     self.stop()
            #     time.sleep(1)
        self.stop()
        self.logging()

    def logging(self):
        """
        Logs the results of the driving session to a CSV file.

        The log is written to a file named 'log.csv' located in the parent directory of the current script.
        The CSV contains a header defined by self.fieldnames and rows from self.result.

        Note: This method assumes that self.fieldnames and self.result are defined elsewhere in the class.
        """
        path = Path(__file__).parents[1].joinpath("log.csv")
        with open(path, "w") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(self.result)

def main():
    """
    Main function to initialize and run the BaseCar's driving session.

    It creates an instance of BaseCar and starts driving with mode 2.
    """
    basecar = BaseCar()
    basecar.fahrmodus1_2(mode=2)



if __name__ == "__main__":
    main()
