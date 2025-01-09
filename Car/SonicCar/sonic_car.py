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
    self.ultrasonic = Ultrasonic()
    super().__init__()

  def get_distance(self): 
    return self.ultrasonic.distance()
  
  def fahrmodus3(self, speed, min_distance):
    print("Starte Fahrmodus 3: fahren bis Hindernis erkannt wird, dann stoppen.")
    self.steering_angle = 90
    fail_counter = 0
    while True:  
       distance = self.get_distance()
       if distance < min_distance and distance > 0:
          print("Hindernis erkannt!")
          self.stop()
          self.ultrasonic.stop()
          break
       elif distance < 0:
          print("Sensor Fehler!")
          fail_counter += 1
          if fail_counter >= 3:
            self.stop()
            self.ultrasonic.stop()
            break
       else:
          self.drive(speed)


  
  def fahrmodus4(self):
     pass

def main():
   car = SonicCar()
   car.fahrmodus3(30, 30)

if __name__ == "__main__":
    main()