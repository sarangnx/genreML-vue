from keras.models import load_model
import cv2
import numpy as np
import sys
import os
import spectrogram as sp
# spectrograms = "/content/drive/My Drive/Data"
# datasetPath = "/content/drive/My Drive/dataset"
modelPath = os.path.abspath("src/predictor/model.h5")
# data_path = "/content/drive/My Drive/Data/"
img_width, img_height = 224, 224

# image= spectrograms + "/Rock/03._Heathens_-_Twenty_One_Pilots_(320kbps)000.png"

cropPath = "/tmp/genre/crop"
if not os.path.exists(cropPath):
    os.makedirs(cropPath)

mp3 = sys.argv[1]
songName = os.path.basename(mp3)

sp.cropSong(mp3,cropPath)

infile = os.path.join(cropPath,songName)
spectPath = "/tmp/genre/spectrogram"
spectrogram = os.path.join(spectPath,songName)

sp.singleSpectrogram(infile,spectPath)

model = load_model(modelPath)
classes = ['Blues','Classical','Country','EDM','Folk','Funk','Hip-Hop','Indie','Jazz','Pop','RnB','Rock']

img = cv2.imread(spectrogram)
img = cv2.resize(img,(224,224))
img = np.reshape(img,[1,224,224,3])

index = model.predict_classes(img)

print (classes[index])

# datagen = ImageDataGenerator(
#     data_format=K.image_data_format(),
#     validation_split=0.8)

# train_generator = datagen.flow_from_directory(
#     data_path,
#     target_size = (img_width,img_height),
#     batch_size = 32,
#     color_mode="rgb",
#     shuffle=True,
#     class_mode = "categorical",
#     subset = "training")

# result = model.predict_generator(
#   train_generator,
#   steps = 10)