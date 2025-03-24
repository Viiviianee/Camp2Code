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
            self.drive(speed=25, steering_angle=int(self.mean_angle))
            print(f"Lenkwinkel: {self.mean_angle}")

    def record(self, flag):
        self.recording = flag
        while self.recording:
            if self.speed > 0:
                self.save_image(self.image_id, self.run_id, self.img_original)
                self.image_id += 1
                time.sleep(0.25)
            else:
                break
        print(f"Not recording. self.recording: {self.recording}, self.running: {self.running}")

if __name__ == "__main__":
    car = Opencvcar()
    car.fahrmodus_cam()