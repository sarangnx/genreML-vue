from keras.models import load_model
import cv2
import numpy as np
import sys
import os
import spectrogram as sp

modelPath = os.path.abspath("src/predictor/model.h5")

img_width, img_height = 224, 224

# PATH TO SAVE THE 30s CROPPED SONG
# cropPath = "/tmp/genre/crop"
# if not os.path.exists(cropPath):
#     os.makedirs(cropPath)
# # PATH TO SAVE THE SPECTROGRAMS
# spectPath = "/tmp/genre/spectrogram"
# if not os.path.exists(spectPath):
#     os.makedirs(spectPath)

def singleMode():
    sp.cropSong(mp3,cropPath)

    infile = os.path.join(cropPath,songName)
    
    spectrogram = os.path.join(spectPath,songName)

    sp.singleSpectrogram(infile,spectPath)

    model = load_model(modelPath)
    classes = ['Blues','Classical','Country','EDM','Folk','Funk','Hip-Hop','Indie','Jazz','Rock']

    img = cv2.imread(spectrogram)
    img = cv2.resize(img,(224,224))
    img = np.reshape(img,[1,224,224,3])

    percentage = model.predict(img)
    index = model.predict_classes(img)

    print(classes[index])


# SINGLE / BATCH MODE SELECTION
mode = sys.argv[1]

# SONG PATH PASSED AS ARGUMENT
mp3 = sys.argv[2]
songName = os.path.basename(mp3)
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
