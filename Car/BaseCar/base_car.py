import click
import time
import numpy as np
import math
import RPi.GPIO as GPIO
import smbus
import json
from pathlib import Path

from basisklassen import Ultrasonic
from basisklassen import Infrared
from basisklassen import FrontWheels
from basisklassen import BackWheels

from basisklassen import Servo
from basisklassen import Motor
from basisklassen import PWM

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
            self.direction = -1
        else:
            self.backwheels.forward()
            self.direction= 1

    def stop(self):
        """
        Stop the car.

        This method stops the car by calling the `stop` method on the `backwheels` object and sets the direction to 0.
        """
        self.backwheels.stop()
        self.direction = 0

def main():
    basecar = BaseCar()
    basecar.speed = 30
    basecar.steering_angle = 135
    basecar.drive()
    time.sleep(2)
    basecar.stop()


if __name__ == "__main__":
    main()
