import sys
import time
import numpy as np
from pathlib import Path

# Dynamically determine the path relative to this file
project_path = Path(__file__).resolve().parent.parent
sys.path.append(str(project_path))

from BaseCar.base_car import BaseCar
from basisklassen import Ultrasonic

class SonicCar(BaseCar):
    """
    A class to represent a car that uses ultrasonic sensors to detect obstacles.
    Inherits from BaseCar and adds functionality to move until an obstacle is detected,
    then stop and log data.
    """

    def __init__(self):
        """
        Initializes the SonicCar instance. Sets the number of digits, initializes
        the ultrasonic sensor, and sets default values for the distance and the steering angle.
        """
        super().__init__()
        self.number_digits = 2
        self.distance = None
        self.ultrasonic = Ultrasonic()

    def get_distance(self):
        """
        Retrieves the current distance measurement from the ultrasonic sensor.

        Returns:
            float: The measured distance from the sensor.
        """
        return self.ultrasonic.distance()

    def fahrmodus3(self, speed, min_distance=30, steering_angle=90):
        """
        Mode 3 of the car's movement: Drive until an obstacle is detected, then stop.

        The car will drive at the specified speed and steering angle until the ultrasonic sensor 
        detects an obstacle within the specified minimum distance. Once the obstacle is detected,
        the car stops, logs the distance, and exits the loop.

        Args:
            speed (int): The speed at which the car should drive.
            min_distance (int, optional): The minimum distance to detect an obstacle. Defaults to 30.
            steering_angle (int, optional): The steering angle of the car. Defaults to 90 (straight).
        """
        self.fieldnames.append("distance_ahead")
        print("Starting driving mode 3: Drive until an obstacle is detected, then stop.")
        if not self.starting_time:
            self.starting_time = time.perf_counter()
        self.steering_angle = steering_angle
        fail_counter = 0
        while True:
            self.distance = self.get_distance()
            if self.distance < min_distance and self.distance > 0:
                print("Obstacle detected!")
                self.stop()
                self.ultrasonic.stop()
                self.result[-1]["distance_ahead"] = self.distance
                break
            elif self.distance < -2:
                print(f"Sensor error! {fail_counter}")
                self.result[-1]["distance_ahead"] = self.distance
                fail_counter += 1
                if fail_counter >= 30:
                    self.stop()
                    self.ultrasonic.stop()
                    self.result[-1]["distance_ahead"] = self.distance
                    break
            else:
                self.drive(speed)
                self.result[-1]["distance_ahead"] = self.distance
        self.logging()

    def fahrmodus4(self, speed, threshold=5):
        """
        Mode 4 of the car's movement: Explore the surroundings until an obstacle is detected, then stop.

        The car will use mode 3 to detect obstacles, then explore the surroundings by randomly 
        changing direction and moving backwards. It will stop after reaching the threshold 
        number of movements or if an obstacle is detected.

        Args:
            speed (int): The speed at which the car should drive.
            threshold (int, optional): The number of exploration steps before stopping. Defaults to 5.
        """
        self.fieldnames.append("distance_ahead")
        print("Starting driving mode 4: Explore until an obstacle is detected, then stop.")
        self.starting_time = time.perf_counter()
        max_steering_angles = [45, 135]
        counter_bw = 0
        while True:
            self.fahrmodus3(speed, 30)
            if self._direction == 0:
                idx = np.random.randint(0, 2)
                self.drive(-30, max_steering_angles[idx])
                self.result[-1]["distance_ahead"] = self.distance
                time.sleep(3)
                counter_bw += 1
                self.stop()
                self.result[-1]["distance_ahead"] = self.distance
                time.sleep(0.5)
            if counter_bw >= threshold:
                break
        self.logging()

def main():
    """
    The main function to create an instance of SonicCar and start the exploration in mode 4.

    It initializes a SonicCar instance and calls fahrmodus4 with a speed of 50.
    """
    car = SonicCar()
    car.fahrmodus4(50)

if __name__ == "__main__":
    main()
