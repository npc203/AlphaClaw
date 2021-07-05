import tensorflow as tf
from tensorflow.keras.datasets import mnist
import autokeras as ak

from sklearn.model_selection import train_test_split
import pickle
import time, os
import random
import cv2
import keras
import numpy as np

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
    label = int(imagePath.split("/")[-1].split("_")[0])
    labels.append(label)

labels = np.reshape(labels, (-1, 0))
(x_train, x_test, y_train, y_test) = train_test_split(
    data, labels, test_size=0.25, random_state=42
)

print(x_test, y_test)
print("Starting")
reg = ak.ImageRegressor(overwrite=True, max_trials=1)
reg.fit(x_train, y_train, epochs=2)

# Predict with the best model.
predicted_y = reg.predict(x_test)
print(predicted_y)


# Evaluate the best model with testing data.
print(reg.evaluate(x_test, y_test))

with open(f"model-{time.time()}.pickle", "wb") as fp:
    pickle.dump(reg, fp)