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

class NNCar(CamCar):
    def __init__(self): 
        super().__init__()
        self.img_path = Path(__file__).parents[0].joinpath("images")
        self.img_size_for_resize = (128, 128)
        self.img_depth = 3
        self.img_shape = (self.img_size_for_resize[0], self.img_size_for_resize[1], self.img_depth)
        self.model = None
        self.weights_path = None


    # def fahrmodus_nn(self):
    #     self.running = True
    #     self.starting_time = time.perf_counter()

    #     while self.running:
    #         self.drive(speed=25, steering_angle=int(self.mean_angle))
    #         print(f"Lenkwinkel: {self.mean_angle}")
    
    def process_img(self):
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
        input_img = Input(shape=self.img_shape)
        x = Conv2D(filters=32, kernel_size=(3,3))(input_img)
        x = Activation("relu")(x)
        x = MaxPooling2D(pool_size=(2,2))(x)
        x = Conv2D(filters=64, kernel_size=(5,5))(x)
        x = Activation("relu")(x)
        x = MaxPooling2D(pool_size=(2,2))(x)
        x = Flatten()(x)
        x = Dense(units=128)(x)
        x = Activation("relu")(x)
        x = Dense(units=128)(x)
        x = Activation("relu")(x)
        x = Dense(units=128)(x)
        x = Activation("relu")(x)
        output = Dense(units=1)(x)

        model = Model(inputs=[input_img], outputs=[output])
        model.compile(loss="mse",
                      optimizer=Adam(learning_rate=0.001),
                      metrics=["mae"])
        self.model = model
        model.summary()

    def train_model(self):
        x = np.load("/home/pi/Desktop/Camp2Code/Car/images/x.npy")
        y = np.load("/home/pi/Desktop/Camp2Code/Car/images/y.npy")
        es_callback = EarlyStopping(
                monitor="val_loss",
                patience=7,
                verbose=1,
                restore_best_weights=True,
                min_delta=0.05)
        
        # sudo apt-get install libhdf5-dev
        # pip install h5py
        model_path = Path(__file__).parents[0].joinpath("model.keras")
        mcp = ModelCheckpoint(str(model_path), monitor="val_loss", save_best_only=True, mode="min")

        x_train, x_test, y_train, y_test = train_test_split(x, y,test_size=0.2)

        history = self.model.fit(
            x=x_train,
            y=y_train,
            epochs=100,
            verbose=1,
            validation_data=(x_test, y_test),
            callbacks = [es_callback, mcp]
        )
    
        plt.plot(history.history['loss'], label = 'loss')
        plt.plot(history.history['val_loss'], label = 'val_loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend(loc='lower right')
        plt.plot(history.history['mae'], label='mae')
        plt.plot(history.history['val_mae'], label = 'val_mae')
        plt.xlabel('Epoch')
        plt.ylabel('Mean absolute error')
        plt.legend(loc='lower right')
        plt.show()  # Wird im Raspberry nicht angezeigt, da zusätzliches Fenster geöffnet wird
    

    def model_loading_weights(self):
        x = np.load("/home/pi/Desktop/Camp2Code/Car/images/x.npy")
        y = np.load("/home/pi/Desktop/Camp2Code/Car/images/y.npy")
        model_path = Path(__file__).parents[0].joinpath("model.keras")
        path = str(model_path)
        self.model = load_model(filepath=path)
        print(self.model(np.expand_dims(x[0], axis=0)))


if __name__ == "__main__":
    car = NNCar()
    #car.process_img()

    # x = np.load("/home/pi/Desktop/Camp2Code/Car/images/x.npy")
    # y = np.load("/home/pi/Desktop/Camp2Code/Car/images/y.npy")
    # print(x.shape)
    # print(y.shape)

    car.build_model()
    car.train_model()

    car.model_loading_weights()



