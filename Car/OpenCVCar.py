from CamCar import CamCar
import time
import uuid

class Opencvcar(CamCar):
    def __init__(self): 
        super().__init__()

    def fahrmodus_cam(self):
        self.running = True
        self.starting_time = time.perf_counter()
        self.image_id = 0  # Initialisiere die Bild-ID
        self.run_id = str(uuid.uuid4())[:8]  # Erstelle eine eindeutige Run-ID

        while self.running:
            # Aktualisiere den Lenkwinkel
            # Fahre mit der aktuellen Geschwindigkeit und dem Lenkwinkel
            self.drive(speed=25, steering_angle=int(self.mean_angle))
            print(f"Lenkwinkel: {self.mean_angle}")
            # Hole das aktuelle Kamerabild
            frame = self.img_original
            if frame is not None:
                self.frame = frame  # Speichere das aktuelle Bild als Attribut

            # #     # Speichere das Bild mit den richtigen Argumenten
            if self.speed > 0:
                self.save_image(self.image_id, self.run_id, frame)
                self.image_id += 1
            else:
                print(f"Bedingung nicht erfüllt: speed={self.speed}, take_image={self.take_image}")

if __name__ == "__main__":
    car = Opencvcar()
    car.fahrmodus_cam()