import keras
from keras import layers
from keras.callbacks import TensorBoard
from sklearn.model_selection import train_test_split
import pickle
import time, os
import random
import cv2

# Constants
path = "tmp/cryptokitties/"

# Prep dataset
data = []
labels = []

imagePaths = sorted(
    filter(lambda x: x.endswith(".png"), map(lambda x: path + x, list(os.listdir(path))))
)
random.seed(42)
random.shuffle(imagePaths)

for imagePath in imagePaths:
    image = cv2.imread(imagePath)
    image = cv2.resize(image, (32, 32)).flatten()
    data.append(image)
    # extract the class label from the image path and update the
    # labels list
    label = imagePath.split(os.path.sep)[-2]
    labels.append(label)

(trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.25, random_state=42)

# Model
input_img = keras.Input(shape=(28, 28, 1))
x = layers.Conv2D(16, (3, 3), activation="relu", padding="same")(input_img)
x = layers.MaxPooling2D((2, 2), padding="same")(x)
x = layers.Conv2D(8, (3, 3), activation="relu", padding="same")(x)
x = layers.MaxPooling2D((2, 2), padding="same")(x)
x = layers.Conv2D(8, (3, 3), activation="relu", padding="same")(x)
encoded = layers.MaxPooling2D((2, 2), padding="same")(x)

# at this point the representation is (4, 4, 8) i.e. 128-dimensional

x = layers.Conv2D(8, (3, 3), activation="relu", padding="same")(encoded)
x = layers.UpSampling2D((2, 2))(x)
x = layers.Conv2D(8, (3, 3), activation="relu", padding="same")(x)
x = layers.UpSampling2D((2, 2))(x)
x = layers.Conv2D(16, (3, 3), activation="relu")(x)
x = layers.UpSampling2D((2, 2))(x)
decoded = layers.Conv2D(1, (3, 3), activation="sigmoid", padding="same")(x)

autoencoder = keras.Model(input_img, decoded)
autoencoder.compile(optimizer="adam", loss="binary_crossentropy")


autoencoder.fit(
    x_train,
    x_train,
    epochs=50,
    batch_size=128,
    shuffle=True,
    validation_data=(x_test, x_test),
    callbacks=[TensorBoard(log_dir="/tmp/autoencoder")],
)


with open(f"model-{time.time()}.pickle", "wb") as fp:
    pickle.dump(autoencoder, fp, protocol=pickle.HIGHEST_PROTOCOL)