from keras.models import load_model
import cv2
import numpy as np
import sys
import os
import spectrogram as sp
import shutil
import threading

# modelPath = os.path.abspath("/src/predictor/model.h5")
modelPath = "src/predictor/model.h5"
model = load_model(modelPath)
classes = ['Blues','Classical','Country','EDM','Folk','Funk','Hip-Hop/Rap','Indie','Jazz','Rock']

img_width, img_height = 224, 224

# Function to Read an Image as a Numpy Array 
def readImage(imagePath):
    img = cv2.imread(imagePath)
    img = cv2.resize(img,(img_width,img_height))
    img = np.reshape(img,[1,img_width,img_height,3])
    return img

# PATH TO SAVE THE 30s CROPPED SONG
cropPath = "/tmp/genre/crop"
# PATH TO SAVE THE 3s SEGMENTS
segPath = "/tmp/genre/segment"
# PATH TO SAVE THE SPECTROGRAMS
spectPath = "/tmp/genre/spectrogram"

def folders():
    # DELETE ALL DIRECTORIES
    if os.path.exists("/tmp/genre"):
        shutil.rmtree("/tmp/genre")

    # CREATE DIRECTORIES
    os.makedirs(cropPath)    
    os.makedirs(spectPath)
    os.makedirs(segPath)

def singleMode(songFile):
    folders()
    # CROP -> SEGMENT -> SPECTROGRAM
    sp.cropSong(songFile,cropPath)
    sp.sliceSongs(cropPath,segPath)

    # ===================================================
    # Call convertToSpectrogram using THREADS instead of
    # directly calling them, to avoid Deadlock when using 
    # librosa.load().
    # ===================================================
    x = threading.Thread(target=sp.convertToSpectrogram, args=(segPath,spectPath))
    x.start()
    x.join()

    files = os.listdir(spectPath)
    files = [file for file in files if file.endswith(".png")]

    prediction_percentage = []
    predicted_class = []

    for file in files:
        
        imageFile = os.path.join(spectPath,file)
        image = readImage(imageFile)

        percentage = model.predict(image)
        prediction_percentage.append(percentage.flatten().tolist())
    
        index = model.predict_classes(image)
        predicted_class.append(np.asscalar(index))
    
    return predicted_class, prediction_percentage

def batchMode():
    pass
# ====================================================================================

# datagen = ImageDataGenerator(
#     data_format=K.image_data_format(),
#     validation_split=0.95)

# train_generator = datagen.flow_from_directory(
#     data_path,
#     target_size = (img_width,img_height),
#     batch_size = 32,
#     color_mode="rgb",
#     shuffle=True,
#     class_mode = "categorical",
#     subset="training")

# model.predict_generator(
#   train_generator,
#   steps=986/32)

