import sys
from pathlib import Path

# Pfad relativ zu dieser Datei dynamisch ermitteln
project_path = Path(__file__).resolve().parent.parent
sys.path.append(str(project_path))
#print(str(project_path))

from BaseCar.base_car import BaseCar
from basisklassen import Ultrasonic

class SonicCar(BaseCar):

  def __init__(self):
    self.sensor = Ultrasonic()
    super().__init__()

  def get_distance(self): 
    return self.sensor.distance()
  
  def fahrmodus3(self):
     pass
  
  def fahrmodus4(self):
     pass

def main():
   car = SonicCar()
   print(car.get_distance())

if __name__ == "__main__":
    main()