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
        self.steering_angle = None
        self.speed = None
        self.direction = None

foo = BaseCar()
print(foo.steering_angle)