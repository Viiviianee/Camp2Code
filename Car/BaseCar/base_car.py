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
from datetime import datetime
from datetime import timezone


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

    def drive(self, speed = None, steering_angle = None):
        if steering_angle:
            self.steering_angle = steering_angle

        if speed:
            self.speed = speed

        self.frontwheels.turn(self._steering_angle)
        print(f"Current value of steering_angle: {self.steering_angle}")

        self.backwheels.speed = abs(self.speed)
        if self.speed < 0:
            self.backwheels.backward()
            self.direction = -1
            print(f"Current value of speed: {self.speed}")
        else:
            self.backwheels.forward()
            self.direction= 1
            print(f"Current value of speed: {self.speed}")

    def stop(self):
        self.speed = 0
        self.backwheels.stop()

    def mode_driving_1(self, speed, time_fw = 3, time_bw = 3, time_sp = 1):
        """Car drives "fahrmodus1": 3sek forwards, 1 sek stop, 3 sek backwards.
        Args:
            speed (int): speed of the motors. Min is -100. Max is 100.
            time_fw (int): duration car drives forward. Default to 3.
            time_bw (int): duration car drives backward. Default to 3.
            time_sp (int): duration car stopps. Default to 1.
        """
        print("----"*30)
        print(datetime.now(tz=timezone.utc).strftime("%H:%M:%S"))
        self.drive(speed, 90)
        time.sleep(time_fw)
        self.stop()
        time.sleep(time_sp)

        print("----"*30)
        print(datetime.now(tz=timezone.utc).strftime("%H:%M:%S"))
        speed = speed * (-1)
        self.drive(speed)
        time.sleep(time_bw)
        self.stop()

    def mode_driving_2(self, speed, time_fw=1, time_cw=8, time_ccw=8, time_bw=1):
        """Car drives "fahrmodus2": 1sek forwards no steering angle, 8 sek with max steering angle clockwise, 8 sek backwards with max steering angle, 1 sek backwards.
                                    1sek forwards no steering angle, 8 sek with max steering angle counterclockwise, 8 sek backwards with max steering angle, 1 sek backwards.
            Args:
                speed (int): speed of the motors. Min is -100. Max is 100.
                time_fw (int): duration car drives forward. Default to 1.
                time_bw (int): duration car drives backward. Default to 1.
                time_cw (int): duration car cw. Default to 8.
                time_ccw (int): duration car ccw. Default to 8.
        """

        print("----"*30)
        print(datetime.now(tz=timezone.utc).strftime("%H:%M:%S"))
        self.drive(speed, 90)
        time.sleep(time_fw)

        print("----"*30)
        print(datetime.now(tz=timezone.utc).strftime("%H:%M:%S"))
        self.drive(steering_angle = 135)
        time.sleep(time_cw)
        self.stop()

        print("----"*30)
        print(datetime.now(tz=timezone.utc).strftime("%H:%M:%S"))
        speed = speed * (-1)
        self.drive(speed, 135)
        time.sleep(time_cw)
        self.stop()

        print("----"*30)
        print(datetime.now(tz=timezone.utc).strftime("%H:%M:%S"))
        self.drive(speed, 90)
        time.sleep(time_bw)
        self.stop()

        print("----"*30)
        print(datetime.now(tz=timezone.utc).strftime("%H:%M:%S"))
        speed = speed * (-1)
        self.drive(speed, 90)
        time.sleep(time_fw)
        self.stop()

        print("----"*30)
        print(datetime.now(tz=timezone.utc).strftime("%H:%M:%S"))
        self.drive(speed, steering_angle = 45)
        time.sleep(time_ccw)
        self.stop()

        print("----"*30)
        print(datetime.now(tz=timezone.utc).strftime("%H:%M:%S"))
        speed = speed * (-1)
        self.drive(speed, steering_angle = 45)
        time.sleep(time_ccw)
        self.stop()

        print("----"*30)
        print(datetime.now(tz=timezone.utc).strftime("%H:%M:%S"))
        self.drive(speed, 90)
        time.sleep(time_bw)
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
        basecar.mode_driving_1(45)

    if modus == 2:
        basecar.mode_driving_2(45)

    # foo = Infrared()
    # while True:
    #     print(foo.read_analog())
    #     time.sleep(2)




if __name__ == "__main__":
    main()
