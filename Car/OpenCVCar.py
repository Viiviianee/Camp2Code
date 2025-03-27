from CamCar import CamCar
import time
import uuid

class Opencvcar(CamCar):
    """
    Eine Klasse, die ein Fahrzeug mit Kamerafunktionalität erweitert und es ermöglicht,
    das Fahrzeug im Fahrmodus zu steuern und Bilder zur Aufzeichnung zu speichern.
    Sie erbt von der `CamCar`-Klasse und bietet zusätzliche Funktionen zum Starten des Fahrmodus
    sowie zum Aufzeichnen von Bildern während der Fahrt.
    """
    def __init__(self):
        """
        Initialisiert das Opencvcar-Objekt und ruft den Konstruktor der Basisklasse `CamCar` auf.

        Dies stellt sicher, dass alle Eigenschaften und Methoden der `CamCar`-Klasse korrekt initialisiert werden.
        """
        super().__init__()

    def fahrmodus_cam(self):
        """
        Startet den Fahrmodus, bei dem das Fahrzeug kontinuierlich mit einer Geschwindigkeit fährt
        und den mittleren Steuerwinkel (`mean_angle`) verwendet, um die Fahrtrichtung anzupassen.

        In diesem Modus wird das Fahrzeug in einer Schleife bewegt, bis der Modus gestoppt wird.
        Die Geschwindigkeit des Fahrzeugs wird auf 25 gesetzt, und der Steuerwinkel wird auf den 
        berechneten mittleren Winkel gesetzt.

        Dieser Modus endet, wenn die `running`-Variable auf `False` gesetzt wird.
        """
        self.running = True
        self.starting_time = time.perf_counter()
        self.image_id = 0  # Initialisiere die Bild-ID
        self.run_id = str(uuid.uuid4())[:8]  # Erstelle eine eindeutige Run-ID

        while self.running:
            self.drive(speed=25, steering_angle=int(self.mean_angle))
            #print(f"Lenkwinkel: {self.mean_angle}")

    def record(self, flag):
        """
        Beginnt oder stoppt die Aufnahme von Bildern basierend auf dem übergebenen Flag.

        Wenn das Flag `True` ist, wird das Fahrzeug fortfahren, Bilder alle 0,25 Sekunden zu speichern,
        solange die Geschwindigkeit des Fahrzeugs größer als 0 ist. Wenn die Geschwindigkeit 0 erreicht,
        wird die Aufnahme gestoppt. Die Bilder werden mit einer fortlaufenden Bild-ID und einer
        einzigartigen Run-ID gespeichert.

        Args:
            flag (bool): Ein Flag, das die Aufnahme steuert. Wenn `True`, wird die Aufnahme gestartet, 
                         andernfalls wird sie gestoppt.
        """
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