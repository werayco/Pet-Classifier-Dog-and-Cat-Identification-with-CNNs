# -*- coding: utf-8 -*-
"""dog vs cat classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jUqPsTIaelq5DuQnTb6qMK72M-NS-vDE
"""

!pip install kaggle

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

!kaggle competitions download -c dogs-vs-cats

# unzipping the downloade file
from zipfile import ZipFile
with ZipFile("dogs-vs-cats.zip","r") as file:
  file.extractall()

with ZipFile("test1.zip","r") as zip:
  zip.extractall()
with ZipFile("train.zip","r") as zip2:
  zip2.extractall()

# importing dependencies
import os
import sys
import time
path = "test1/"
train_data = os.listdir("train")
print(train_data[0:5])
test_data = os.listdir("test1")
print(test_data[0:5])

curr_dir,sub_dir,files_in_curr_dir = next(os.walk("test1"))

import numpy as np
from PIL import Image
import matplotlib.image as img
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from google.colab.patches import cv2_imshow
from keras.models import Sequential
from keras.layers import Conv2D,Dense,Flatten,Dropout,MaxPooling2D

# lets display an image of a dog
image = img.imread("train/cat.8821.jpg")
image1 = plt.imshow(image)
plt.show()



"""dog = []
cat = []
for image1 in train_data:
  if image1[0:3] == "cat":
    cat.append(image1):
  elif image1[0:3] == "dog":
      dog.append(image1)

"""

dogg = []
catt = []

for image1 in train_data:
    if image1[0:3] == "cat":
        catt.append(image1)
    elif image1[0:3] == "dog":
        dogg.append(image1)


# resizing all the images
path_for_all = "train/"

#creating a directory named resized
os.mkdir("resized")


output_path = "/content/resized/"
for every_image in dogg:
  an_image = Image.open(path_for_all + every_image)
  an_image = an_image.resize((224,224))
  an_image.save(output_path + every_image)    #saving all the reshaped dog images


for every_image in catt:
  an_image = Image.open(path_for_all + every_image)
  an_image = an_image.resize((224,224))
  an_image.save(output_path + every_image)


import glob
import cv2
import numpy as np


file_extension = ["png","jpg"]
file_paths = "/content/resized"

files=[]
[files.extend(glob.glob(file_paths + "*." + e)) for e in file_extension]


dog_cat = dogg + catt

path = "/content/resized/"
list_image = []
for every_image in dog_cat:
   image_1 = cv2.imread(path + every_image)
   list_image.append(image_1)
x_data = np.array(list_image)

# or we can aslo use this
# x_data = np.array([cv2.imread(path every_image) for every_image in dog_cat])

x_data.shape



# using MinMaxScalar to scaale the data from 0 - 255
scaled_data=x_data/255
label=[]
for x in dogg:
  if x[0:3]=="dog":
    label.append(1)
for y in catt:
  if y[0:3] =="cat":
    label.append(0)

label[100]     #checking the first 100 labels



# in this section, transfer learning is used, and the pre-trained model we use is MobileNet_V2
import tensorflow_hub as hub
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split


model_link = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4"
pretrained_model_layer = hub.KerasLayer(model_link, input_shape=(224,224,3), trainable=False)

model = Sequential([
    pretrained_model_layer,
    Dense(2,activation="sigmoid")])

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
x_train,y_train,x_test,y_test=train_test_split(x_data,label,random_state=40,test_size=0.3)

pred=model.fit(x_train,y_train,validation_set=0.1,epochs=5)
score,acc = model.evaluate(x_test,y_test)

print(f"the score of the model is {score} and the accuracy is {acc}")

"""How to save the model

"""

model.save("your_model_name.h5")
