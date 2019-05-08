from keras.models import load_model
import cv2
import numpy as np
import sys
import os

# spectrograms = "/content/drive/My Drive/Data"
# datasetPath = "/content/drive/My Drive/dataset"
modelPath = os.path.abspath("src/predictor/model.h5")
# data_path = "/content/drive/My Drive/Data/"
img_width, img_height = 224, 224

# image= spectrograms + "/Rock/03._Heathens_-_Twenty_One_Pilots_(320kbps)000.png"

image = sys.argv[1]

model = load_model(modelPath)
classes = ['Blues','Classical','Country','EDM','Folk','Funk','Hip-Hop','Indie','Jazz','Pop','RnB','Rock']

img = cv2.imread(image)
img = cv2.resize(img,(224,224))
img = np.reshape(img,[1,224,224,3])

classes = model.predict_classes(img)

print (classes)

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