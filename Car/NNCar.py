from CamCar import CamCar
import time
from pathlib import Path
import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Activation
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers import Optimizer
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.models import save_model
from tensorflow.keras.models import load_model
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import tflite_runtime.interpreter as tflite

class NNCar(CamCar):
    """
    Eine Klasse, die ein neuronales Netzwerk für ein autonomes Fahrzeug repräsentiert, 
    das mit Bildern arbeitet, um Steuerbefehle zu generieren. 
    Diese Klasse erbt von der CamCar-Klasse und implementiert Funktionen zur 
    Bilderverarbeitung, Modellbildung, -training und -nutzung.
    """
    def __init__(self):
        """
        Initialisiert das NNCar-Objekt und lädt das TFLite-Modell, wenn es existiert.
        Die Größe und Form der Bilder wird ebenfalls festgelegt, sowie der Pfad 
        zu den Bildern und das Modell.
        """
        super().__init__()
        self.img_path = Path(__file__).parents[0].joinpath("images")
        self.img_size_for_resize = (128, 128)
        self.img_depth = 3
        self.img_shape = (self.img_size_for_resize[0], self.img_size_for_resize[1], self.img_depth)

        _model_path = str(Path(__file__).parents[0].joinpath("TFLite_Modell.tflite"))
        if os.path.exists(_model_path):
            self.interpreter = tflite.Interpreter(model_path="/home/pi/Camp2Code/Car/TFLite_Modell.tflite")
        else:
            print("TFLite_Modell liegt nicht vor.")
            self.interpreter = None

    def process_img(self):
        """
        Lädt alle Bilder im angegebenen Verzeichnis, konvertiert sie in ein geeignetes Format 
        und speichert die Bilddaten sowie die Labels als .npy-Dateien.
        Der Label wird aus dem Dateinamen extrahiert.
        """
        if os.path.exists(self.img_path):
            images = []
            labels = []
            for filename in os.listdir(self.img_path):
                if filename.endswith(".jpg"):
                    label = filename.split(".")[0]
                    label = label.split("_")[-1]
                    label = label[-3:]
                    labels.append(label)

                    img = cv2.imread(str(self.img_path) + "/" + filename)
                    img = cv2.resize(img, self.img_size_for_resize)
                    img = img/ 255
                    images.append(img)

            labels = [float(f) for f in labels]
            labels = np.array(labels)
            images = np.array(images)
            with open(str(self.img_path) + "/" + "x.npy", "wb") as file:
                np.save(file, images)
            with open(str(self.img_path) + "/" + "y.npy", "wb") as file:
                np.save(file, labels)
        else:
            print("Image folder does not exist on this file level")

    def build_model(self):
        """
        Erstellt und kompiliert ein Convolutional Neural Network (CNN)-Modell für die 
        Vorhersage eines kontinuierlichen Wertes, wie z. B. den Lenkwinkel eines Fahrzeugs.
        """
        input_img = Input(shape=self.img_shape)
        x = Conv2D(filters=32, kernel_size=(3,3))(input_img)
        x = Activation("relu")(x)
        x = MaxPooling2D(pool_size=(2,2))(x)
        x = Conv2D(filters=48, kernel_size=(5,5))(x)
        x = Activation("relu")(x)
        x = Conv2D(filters=64, kernel_size=(5,5))(x)
        x = Activation("relu")(x)
        x = MaxPooling2D(pool_size=(2,2))(x)
        x = Flatten()(x)
        x = Dense(units=128)(x)
        x = Activation("relu")(x)
        x = Dense(units=64)(x)
        x = Activation("relu")(x)
        x = Dense(units=32)(x)
        x = Activation("relu")(x)
        output = Dense(units=1)(x)

        model = Model(inputs=[input_img], outputs=[output])
    
        # # Keras Sequntial API
        # model = tf.keras.Sequential(name='BeispielModell') 
        # # Convolution Layers 
        # # elu: Expenential Linear Unit, similar to leaky Relu 
        # model.add(Conv2D(24, (5, 5), strides=(2, 2), input_shape=(100, 200, 3), activation='elu')) 
        # model.add(Conv2D(36, (5, 5), strides=(2, 2), activation='elu'))
        # model.add(Conv2D(48, (5, 5), strides=(2, 2), activation='elu'))
        # model.add(Conv2D(64, (3, 3), activation='elu')) 
        # model.add(Dropout(0.2)) # more robustness 
        # model.add(Conv2D(64, (3, 3), activation='elu')) 
        # # Fully Connected Layers 
        # model.add(Flatten()) 
        # model.add(Dropout(0.2)) # more robustness 
        # model.add(Dense(100, activation='elu')) 
        # model.add(Dense(50, activation='elu')) 
        # model.add(Dense(10, activation='elu'))
        # # Output Layer: turning angle
        # model.add(Dense(1)) 
        
        model.compile(loss="mse",
                      optimizer=Adam(learning_rate=0.001),
                      metrics=["mae"])
        self.model = model
        model.summary()

    def train_model(self):
        """
        Trainiert das Modell mit den vorbereiteten Trainingsdaten und validiert es 
        mit einem Testdatensatz. Während des Trainings werden die Verlustfunktionen 
        und die mittlere absolute Fehler (MAE) über die Epochen hinweg angezeigt.
        Verwendet EarlyStopping und ModelCheckpoint für die Modellverbesserung.
        """
        x_path = self.img_path = Path(__file__).parents[0].joinpath("images", "x.npy")
        y_path = self.img_path = Path(__file__).parents[0].joinpath("images", "y.npy")
        x = np.load(x_path)
        y = np.load(y_path)
        es_callback = EarlyStopping(
                monitor="val_loss",
                patience=7,
                verbose=1,
                restore_best_weights=True,
                min_delta=0.05)

        # sudo apt-get install libhdf5-dev
        # pip install h5py
        model_path = Path(__file__).parents[0].joinpath("model.keras")
        mcp = ModelCheckpoint(str(model_path), monitor="val_loss", mode="min")

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

        history = self.model.fit(
            x=x_train,
            y=y_train,
            epochs=100,
            verbose=1,
            batch_size=64,
            validation_data=(x_test, y_test),
            callbacks=[es_callback, mcp]
        )

        plt.plot(history.history['loss'], label = 'loss')
        plt.plot(history.history['val_loss'], label = 'val_loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend(loc='lower right')
        plt.show()
        plt.plot(history.history['mae'], label='mae')
        plt.plot(history.history['val_mae'], label = 'val_mae')
        plt.xlabel('Epoch')
        plt.ylabel('Mean absolute error')
        plt.legend(loc='lower right')
        plt.show()  # Wird im Raspberry nicht angezeigt, da zusätzliches Fenster geöffnet wird

    def model_loading(self):
        """
        Lädt das vortrainierte Modell und führt eine Vorhersage für ein Beispielbild durch.
        Die Eingabedaten werden aus den gespeicherten .npy-Dateien geladen.
        """
        x = str(Path(__file__).parents[0].joinpath("images", "x.npy"))
        x = np.load(x)
        y = str(Path(__file__).parents[0].joinpath("images", "y.npy"))

        model_path = Path(__file__).parents[0].joinpath("model.keras")
        path = str(model_path)
        self.model = load_model(filepath=path)
        test = self.model(np.expand_dims(x[10], axis=0))
        test = test.numpy()
        print(test[0][0])

    def model_drive(self):
        """
        Führt das autonome Fahrzeug basierend auf der Vorhersage des Modells.
        Verwendet das TFLite-Modell, um Bilder in Steuerbefehle (Lenkwinkel) umzuwandeln.
        Die Fahrt wird kontinuierlich mit einer festen Geschwindigkeit ausgeführt.
        """
        self.starting_time = time.perf_counter()
        self.running = True
        while self.running:
            frame = self.img_original
            frame = cv2.resize(frame, self.img_size_for_resize)
            frame = frame / 255
            frame = frame.astype(np.float32)
            frame = frame.reshape(1, self.img_size_for_resize[0], self.img_size_for_resize[1], self.img_depth)
            input_details = self.interpreter.get_input_details()
            output_details = self.interpreter.get_output_details()
            self.interpreter.allocate_tensors()
            self.interpreter.set_tensor(input_details[0]['index'], frame)
            self.interpreter.invoke()
            output_data = self.interpreter.get_tensor(output_details[0]['index'])
            self.mean_angle = output_data[0][0]
            self.drive(speed=25, steering_angle=int(self.mean_angle))
            print(f"Lenkwinkel: {self.mean_angle}")

    @staticmethod
    def convert_model_to_tflite():
        """
        Konvertiert das Keras-Modell in das TFLite-Format und speichert es als .tflite-Datei.
        Dies ist nützlich für die Ausführung des Modells auf einem Edge-Gerät wie einem Raspberry Pi.
        """
        model_path = Path(__file__).parents[0].joinpath("model.keras")
        model_path = str(model_path)
        loaded_model = load_model(model_path)
        converter = tf.lite.TFLiteConverter.from_keras_model(loaded_model)
        tflite_model = converter.convert()
        with open("TFLite_Modell.tflite", 'wb') as f:
            f.write(tflite_model)


if __name__ == "__main__":
    car = NNCar()
    # car.process_img()
    # car.build_model()
    # car.train_model()
    #car.convert_model_to_tflite()
