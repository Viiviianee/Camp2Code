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
        path = Path(__file__).parents[0].joinpath("config.json")
        with open(path, "r") as f:
                data = json.load(f)
                turning_offset = data["turning_offset"]
                forward_A = data["forward_A"]
                forward_B = data["forward_B"]
        self.frontwheels = FrontWheels(turning_offset=turning_offset)
        self.backwheels = BackWheels(forward_A = forward_A, forward_B = forward_B )


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
        self.backwheels.speed = abs(self.speed)  # Methods backwards and forwards are accessing on backwheels.speed which is on default 0
        if self._speed < 0:
            self.backwheels.backward()
            self._direction = -1
        else:
            self.backwheels.forward()
            self._direction = 1
        self.result_t = {#"counter": cnt,
                        "time": str(datetime.now(tz=timezone.utc).strftime("%H:%M:%S")),
                        "speed": self.speed,
                        "steering_angle": self.steering_angle,
                        "direction": self.direction,
                        #"distance_ahead": distance_ahead
                        }
        self.result.append(self.result_t)


    def stop(self):
        """
        Stop the car.

        This method stops the car by calling the `stop` method on the `backwheels` object and sets the direction to 0.
        """
        self.backwheels.stop()
        self._direction = 0
        self.result_t = {#"counter": cnt,
                        "time": str(datetime.now(tz=timezone.utc).strftime("%H:%M:%S")),
                        "speed": self.speed,
                        "steering_angle": self.steering_angle,
                        "direction": self.direction,
                        #"distance_ahead": distance_ahead
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


    def fahrmodus2(self, speed, time_fw=1, time_cw=8, time_ccw=8, time_bw=1):
        """Car drives "fahrmodus2": 1sek forwards no steering angle, 8 sek with max steering angle clockwise, 8 sek backwards with max steering angle, 1 sek backwards.
                                    1sek forwards no steering angle, 8 sek with max steering angle counterclockwise, 8 sek backwards with max steering angle, 1 sek backwards.
            Args:
                speed (int): speed of the motors. Min is -100. Max is 100.
                time_fw (int): duration car drives forward. Default to 1.
                time_bw (int): duration car drives backward. Default to 1.
                time_cw (int): duration car cw. Default to 8.
                time_ccw (int): duration car ccw. Default to 8.
            """
        self.drive(speed, 90)
        time.sleep(time_fw)
        self.drive(steering_angle=135)
        time.sleep(time_cw)
        self.stop()
        speed = speed * (-1)
        self.drive(speed)
        time.sleep(time_cw)
        self.drive(speed, 90)
        time.sleep(time_bw)
        self.stop()
        speed = speed * (-1)
        self.drive(speed, 90)
        time.sleep(time_fw)
        self.drive(steering_angle=45)
        time.sleep(time_ccw)
        self.stop()
        speed = speed * (-1)
        self.drive(speed)
        time.sleep(time_ccw)
        self.drive(speed, 90)
        time.sleep(time_bw)
        self.stop()
        self.logging()

    def logging(self):
      #Geschwindigkeit über self._speed
      #Fahrrichtung über self.__direction
      #Lenkwinkel über self._steering_angle
      #'get_distance()' return value
      #Schreiben in JSON / CSV
        path = Path(__file__).parents[1].joinpath("log.csv")
        with open(path, "w") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(self.result) #result = list of dict

def main():
    basecar = BaseCar()
    basecar.fahrmodus1(30)



if __name__ == "__main__":
    main()
