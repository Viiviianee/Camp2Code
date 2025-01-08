from base_car import BaseCar
import time

def fahrmodus1(speed, time_fw = 3, time_bw = 3, time_sp = 1):
    """Car drives "fahrmodus1": 3sek forwards, 1 sek stop, 3 sek backwards.

        Args:
            speed (int): speed of the motors. Min is -100. Max is 100. 
            time_fw (int): duration car drives forward. Default to 3.
            time_bw (int): duration car drives backward. Default to 3.
            time_sp (int): duration car stopps. Default to 1.

        
        """
    car = BaseCar()
    #fahrt forwärts für 3 sek
    car.speed = speed
    car.steering_angle = 90
    car.drive()
    time.sleep(time_fw)
    car.stop()
    time.sleep(time_sp)
    #fahrt rückwärts für 3 sek
    car.speed = speed * (-1)
    car.drive()
    time.sleep(time_bw)
    car.stop()


def main():
    fahrmodus1(45)
    


if __name__ == "__main__":
    main()