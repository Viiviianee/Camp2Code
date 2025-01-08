import click
import time
import numpy as np
import math
import RPi.GPIO as GPIO
import smbus
import json
import pdb
import os
from pathlib import Path


from basisklassen import Ultrasonic
from basisklassen import Infrared
from basisklassen import FrontWheels
from basisklassen import BackWheels

from basisklassen import Servo
from basisklassen import Motor
from basisklassen import PWM

class BaseCar:
    def __init__(self):
        self._steering_angle = 90
        self._speed = 0
        self.direction = 0
        self.backwheels = BackWheels()
        path = Path(__file__).parents[0].joinpath("config.json")
        with open(path, "r") as f:
                data = json.load(f)
                turning_offset = data["turning_offset"]
        self.frontwheels = FrontWheels(turning_offset=turning_offset)

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

    def drive(self, new_val_steering_angle = None, new_val_speed = None ):
        if new_val_steering_angle:
            self.steering_angle = new_val_steering_angle

        if new_val_speed:
            self.speed = new_val_speed

        self.frontwheels.turn(self._steering_angle)
        print(f"Current value of steering_angle: {self.steering_angle}")

        self.backwheels.speed = abs(self.speed)
        if self.speed < 0:
            self.backwheels.forward()
            self.direction = -1
            print(f"Current value of speed: {self.speed}")
        else:
            self.backwheels.backward()
            self.direction= 1
            print(f"Current value of speed: {self.speed}")

    def stop(self):
        self.speed = 0
        self.backwheels.stop()

    def mode_driving_1(self):
        self.speed = 30
        self.steering_angle = 90
        time.sleep(0.5)

        self.drive()
        time.sleep(3)

        self.stop()
        time.sleep(0.5)

        self.speed = -30
        self.drive()
        time.sleep(3)

        self.stop()

    def mode_driving_2(self):
        self.speed = 30
        self.steering_angle = 90
        time.sleep(0.5)

        self.drive()
        time.sleep(1)

        self.stop()
        self.speed = 30
        self.steering_angle = 135
        time.sleep(0.5)

        self.drive()
        time.sleep(8)

        self.stop()
        time.sleep(0.5)

        self.speed = -30
        self.drive()
        time.sleep(8)

        self.stop()
        time.sleep(0.5)

        self.speed = 30
        self.steering_angle = 45
        self.drive()
        time.sleep(8)

        self.stop()
        time.sleep(0.5)

        self.speed = -30
        self.drive()
        time.sleep(8)

        self.steering_angle = 90
        self.stop()



@click.command()
@click.option('--modus', '--m', type=int, default=None, help="Auswahl Fahrtmodus")
def main(modus):
    modi = {
        1: '3s Geradeausfahrt, 1s Pause, 3s Rückwärtsfahrt',
        2: '1s Geradeausfahrt, 8s im Uhrzeigersinn + zurück, 8s gegen Uhrzeigersinn + zurück'
        }

    if modus == None:
        print('----' * 20)
        print('Auswahl:')
        for m in modi.keys():
            print(f"{m} - {modi[m]}")
        print('----' * 20)

    while modus == None:
        try:
            modus_list = list(modi.keys())
            modus = int(input('Wähle  (Andere Taste für Abbruch): ? '))
            break
        except:
            print('Getroffene Auswahl nicht möglich.')
            quit()
    basecar = BaseCar()
    if modus == 1:
        basecar.mode_driving_1()

    if modus == 2:
        basecar.mode_driving_2()

    foo = Infrared()
    while True:
        print(foo.read_analog())
        time.sleep(2)




if __name__ == "__main__":
    main()
