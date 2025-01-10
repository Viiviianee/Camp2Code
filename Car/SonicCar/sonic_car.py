import sys
import time
import numpy as np
from pathlib import Path

# Pfad relativ zu dieser Datei dynamisch ermitteln
project_path = Path(__file__).resolve().parent.parent
sys.path.append(str(project_path))
#print(str(project_path))

from BaseCar.base_car import BaseCar
from basisklassen import Ultrasonic

class SonicCar(BaseCar):

  def __init__(self):
    super().__init__()
    self.fieldnames.append("distance_ahead")
    self.distance = None
    self.ultrasonic = Ultrasonic()

  def get_distance(self):
    return self.ultrasonic.distance()

  def fahrmodus3(self, speed, min_distance = 30, steering_angle = 90):
    print("Starte Fahrmodus 3: fahren bis Hindernis erkannt wird, dann stoppen.")
    self.steering_angle = steering_angle
    fail_counter = 0
    while True:
       self.distance = self.get_distance()
       if self.distance < min_distance and self.distance > 0:
          print("Hindernis erkannt!")
          self.stop()
          self.ultrasonic.stop()
          self.result[-1]["distance_ahead"] = self.distance
          break
       elif self.distance < -2:
          print(f"Sensor Fehler! {fail_counter}")
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



  def fahrmodus4(self, speed, threshold = 5):
   print("Starte Fahrmodus 4: Erkunden bis Hindernis erkannt wird, dann stoppen.")
   max_steering_angles = [45, 135]
   counter_bw = 0
   while True:
      self.fahrmodus3(speed,30)
      if self._direction == 0:
         idx = np.random.randint(0,2)
         self.drive(-30,max_steering_angles[idx])
         self.result[-1]["distance_ahead"] = self.distance
         time.sleep(3)
         counter_bw += 1
         self.stop()
         self.result[-1]["distance_ahead"] = self.distance
         time.sleep(0.5)
      if counter_bw >= threshold:
         self.stop()
         self.result[-1]["distance_ahead"] = self.distance
         break
   self.logging()


def main():
   car = SonicCar()
   car.fahrmodus4(50)

if __name__ == "__main__":
    main()
