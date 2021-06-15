import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image


n = 0
m = 0
x_dim = 32
y_dim = 32
counter = 0
for filename in os.listdir("train_dataset"):

    cropped_image = image.crop(box)
    image = Image.open(filename)
    imgwidth, imgheight = image.size
    for i in range(0,imgheight,x_dim):
        for j in range(0,imgwidth,y_dim):
            box = (j, i, j+x_dim, i+y_dim)
            a = image.crop(box)
            try:
                print("Hello")
            except:
                pass
            counter = counter + 1;

lenet_5_model = keras.models.Sequential([
    keras.layers.Conv2D(6, kernel_size=5, strides=1,  activation='tanh', input_shape=train_x[0].shape, padding='same'), #C1
    keras.layers.AveragePooling2D(), #S2
    keras.layers.Conv2D(16, kernel_size=5, strides=1, activation='tanh', padding='valid'), #C3
    keras.layers.AveragePooling2D(), #S4
    keras.layers.Flatten(), #Flatten
    keras.layers.Dense(120, activation='tanh'), #C5
    keras.layers.Dense(84, activation='tanh'), #F6
    keras.layers.Dense(10, activation='softmax') #Output layer
    ])

lenet_5_model.compile( optimizer= 'adam' , loss=keras.losses.sparse_categorical_crossentropy, metrics=['accuracy'])


lenet_5_model.fit(train_x, train_y, epochs=5, validation_data=(val_x, val_y))
lenet_5_model.evaluate(test_x, test_y)