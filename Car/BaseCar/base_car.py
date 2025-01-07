import click
import time
import numpy as np
import math
import RPi.GPIO as GPIO
import smbus
import json


from basisklassen import Ultrasonic
from basisklassen import Infrared
from basisklassen import FrontWheels
from basisklassen import BackWheels

from basisklassen import Servo
from basisklassen import Motor
from basisklassen import PWM

class BaseCar:
    def __init__(self):
        self._steering_angle = None
        self._speed = None
        self.direction = 0
        self.backwheels = BackWheels()
        self.frontwheels = FrontWheels()

    @property
    def steering_angle(self):
        return self._steering_angle
    
    @steering_angle.setter
    def steering_angle(self,value):
        self._steering_angle=value
        if value < 45:
            self._steering_angle = 45
        if value > 135:
            self._steering_angle = 135


    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self,value):
        self._speed=value
        if value < -100:
            self._speed = -100
        if value > 100:
            self._speed = 100

    def drive(self):
        self.backwheels.speed(self._speed)
        self.frontwheels.turn(self._steering_angle)
        if self._speed < 0:
            self.backwheels.backward()
            self.direction= -1
        else:
            self.backwheels.forward()
            self.direction= 1 
    
    def stop(self):
        self._speed= 0
        self.backwheels.stop()
        self.direction= 0

basecar = BaseCar()
print(basecar.steering_angle)
basecar.steering_angle=120
print(basecar.steering_angle)