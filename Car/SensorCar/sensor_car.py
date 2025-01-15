import sys
import time
import json
from pathlib import Path

project_path = Path(__file__).resolve().parent.parent
sys.path.append(str(project_path))

from basisklassen import Infrared
from BaseCar.base_car import BaseCar
from SonicCar.sonic_car import SonicCar

class SensorCar(SonicCar):

    def __init__(self):
        """
        SensorCar is a subclass of SonicCar that uses an infrared sensor to follow a line.

        The class initializes the infrared sensor with calibration values from a configuration file.
        It inherits all functionalities from SonicCar and adds the ability to follow a line using the infrared sensor.

        Attributes:
            infrared (Infrared): An instance of the Infrared class used to read sensor data.

        Methods:
            fahrmodus5(): Car tries to follow a line with the use of the infrared sensor. 
            If the end of the line or no line is reached, the car stops.
    """
        super().__init__()
        path = project_path.joinpath("BaseCar", "config.json")
        with open(path, "r") as f:
            data = json.load(f)
            cal_vals = data["cal_vals"]
        self.infrared = Infrared(cal_vals)
                


    def fahrmodus5(self, speed=30, maneuvering=False):
        """
        Car tries to follow a line with the use of the infrared sensor. If the end of the line or no line is reached, the car stops.

        The function continuously reads data from the infrared sensor and adjusts the car's steering angle based on the sensor data.
        If all sensor values are zero for a certain number of iterations, the car stops.
        If any sensor value is greater than zero, the car drives forward and adjusts its steering angle based on the sensor data.

        Attributes:
            starting_time (float): The time when the function starts.
            cnt (int): Counter to track the number of consecutive iterations with no line detected.
            sensor_data (list): List of sensor readings from the infrared sensor.
            sensor (list): Stores the current sensor data.
            steering_angle (float): The angle at which the car's steering is set.

        Methods:
            stop(): Stops the car.
            drive(speed): Drives the car at the specified speed.
            logging(): Logs the current state of the car.
            infrared.read_digital(): Reads the digital data from the infrared sensor.
    """
        self.starting_time = time.perf_counter()
        cnt = 0
        sensor_data_save = [0,0,0,0,0]
        while True :

            sensor_data = self.infrared.read_digital()
            self.sensor = sensor_data            
            if all(t == 0 for t in sensor_data):
                cnt += 1
                if cnt > 100:
                    if sensor_data_save == [0,0,0,0,0]:
                        self.stop()
                        break
                    elif sensor_data_save == [1,0,0,0,0]:
                        self.drive(speed *(-1), steering_angle=135)
                        time.sleep(0.5)
                    elif sensor_data_save == [0,0,0,0,1]:
                        self.drive(speed *(-1), steering_angle=45)
                        time.sleep(0.5)

            if any(t > 0 for t in sensor_data):
                cnt = 0
                print("Fahren")
                self.drive(speed)
                self.logging()
                if sensor_data == [1,0,0,0,0]:
                    self.steering_angle = 45
                    if maneuvering == True:
                        sensor_data_save = sensor_data
                elif sensor_data == [0,1,0,0,0]:
                    self.steering_angle = 67.5
                    sensor_data_save = [0,0,0,0,0]
                elif sensor_data == [0,0,1,0,0]:
                    self.steering_angle = 90
                    sensor_data_save = [0,0,0,0,0]
                elif sensor_data == [0,0,0,1,0]:
                    self.steering_angle = 112.5
                    sensor_data_save = [0,0,0,0,0]
                elif sensor_data == [0,0,0,0,1]:
                    self.steering_angle = 135
                    if maneuvering == True:
                        sensor_data_save = sensor_data

    def fahrmodus6(self, speed=30, maneuvering=True):
        self.fahrmodus5(speed, maneuvering)
def main():
    sensorcar = SensorCar()
    sensorcar.fahrmodus6()
    time.sleep(5)
    sensorcar.stop()
    

if __name__ == "__main__":
    main()