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
    car.drive(speed, 90)
    time.sleep(time_fw)
    car.stop()
    time.sleep(time_sp)
    #fahrt rückwärts für 3 sek
    speed = speed * (-1)
    car.drive(speed)
    time.sleep(time_bw)
    car.stop()


#Fahrmodus2 Kreisfahrt mit maximalem Lenkwinkel
def fahrmodus2(speed, time_fw=1, time_cw=8, time_ccw=8, time_bw=1):
    """Car drives "fahrmodus2": 1sek forwards no steering angle, 8 sek with max steering angle clockwise, 8 sek backwards with max steering angle, 1 sek backwards.
                                1sek forwards no steering angle, 8 sek with max steering angle counterclockwise, 8 sek backwards with max steering angle, 1 sek backwards.
        Args:
            speed (int): speed of the motors. Min is -100. Max is 100. 
            time_fw (int): duration car drives forward. Default to 1.
            time_bw (int): duration car drives backward. Default to 1.
            time_cw (int): duration car cw. Default to 8.
            time_ccw (int): duration car ccw. Default to 8.

        
        """
    car = BaseCar()
    car.drive(speed, 90)
    time.sleep(time_fw)
    car.drive(steering_angle = 135)
    time.sleep(time_cw)
    car.stop()
    speed = speed * (-1)
    time.sleep(time_cw)
    car.drive(speed, 90)
    time.sleep(time_bw)
    car.stop()
    speed = speed * (-1)
    car.drive(speed, 90)
    time.sleep(time_fw)
    car.drive(steering_angle = 45)
    time.sleep(time_ccw)
    car.stop()
    speed = speed * (-1)
    time.sleep(time_ccw)
    car.drive(speed, 90)
    time.sleep(time_bw)
    car.stop()

def main():
    #fahrmodus1(45)
    fahrmodus2(45)


if __name__ == "__main__":
    main()