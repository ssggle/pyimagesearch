# -----------------------------
#   USAGE
# -----------------------------
# python train_conv_autoencoder.py

# -----------------------------
#   IMPORTS
# -----------------------------
# Set the matplotlib backend so figures can be saved in the background
import matplotlib
matplotlib.use("Agg")
# Import the necessary packages
from pyimagesearch.convautoencoder import ConvAutoEncoder
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.datasets import mnist
import matplotlib.pyplot as plt
import numpy as np
import argparse
import cv2


# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--samples", type=int, default=8, help="# number of samples to visualize when decoding")
ap.add_argument("-o", "--output", type=str, default="output.png", help="path to output visualization file")
ap.add_argument("-p", "--plot", type=str, default="plot.png", help="path to output plot file")
args = vars(ap.parse_args())

# Initialize the number of epochs to train for and batch size
EPOCHS = 25
BS = 32

# Load the MNIST dataset
print("[INFO] Loading the MNIST dataset...")
((trainX, _), (testX, _)) = mnist.load_data()

# Add a channel dimension to every image in the dataset, then scale the pixel intensities to the range [0, 1]
trainX = np.expand_dims(trainX, axis=-1)
testX = np.expand_dims(testX, axis=-1)
trainX = trainX.astype("float32") / 255.0
testX = testX.astype("float32") / 255.0

# Construct the convolutional autoencoder
print("[INFO] Building the autoencoder...")
(encoder, decoder, autoencoder) = ConvAutoEncoder.build(28, 28, 1)
opt = Adam(lr=1e-3)
autoencoder.compile(loss="mse", optimizer=opt)

# Train the convolution autoencoder
H = autoencoder.fit(trainX, trainX, validation_data=(testX, testX), epochs=EPOCHS, batch_size=BS)

# Construct a plot that plots and saves the training history
N = np.arange(0, EPOCHS)
plt.style.use("ggplot")
plt.figure()
plt.plot(N, H.history["loss"], label="train_loss")
plt.plot(N, H.history["val_loss"], label="val_loss")
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="lower left")
plt.savefig(args["plot"])

# Use the convolutional autoencoder to make predictions on the testing images and initialize the list of output images
print("[INFO] Making predictions...")
decoded = autoencoder.predict(testX)
outputs = None

# Loop over the number of output samples
for i in range(0, args["samples"]):
    # Grab the original image and reconstructed image
    original = (testX[i] * 255).astype("uint8")
    recon = (decoded[i] * 255).astype("uint8")
    # Stack the original and reconstructed image side-by-side
    output = np.hstack([original, recon])
    # If the outputs array is empty, initialize it as the current side-by-side image display
    if outputs is None:
        outputs = output
    # Otherwise, vertically stack the outputs
    else:
        outputs = np.vstack([outputs, output])

# Save the outputs image to disk
cv2.imwrite(args["output"], outputs)
