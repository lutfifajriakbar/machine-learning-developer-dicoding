# -*- coding: utf-8 -*-
"""Proyek Akhir : Image Classification Model Deployment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1b5hbUNYdaSVuhj4WWBArqBxdEt1dwlCk

# Data Diri
### **Nama** : 
Lutfi Fajri Akbar
### **No. Register** :
1494037162101-2551
### **Username Dicoding**:
lutfifajri02
### **E-mail**:
ltfffajri@gmail.com

# Data Acquisition From Kaggle
"""

!pip install Kaggle
!mkdir ~/.kaggle

! cp kaggle.json ~/.kaggle/
! chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d alessiocorrado99/animals10

"""# Extract Dataset """

import zipfile, os

local_zip = '/content/animals10.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/content')
zip_ref.close()

"""# Cek Label Yang Dimiliki Dataset"""

training_dir = os.path.join('/content/raw-img')

print(os.listdir(training_dir))
# Terjemahan Label = "cane": "dog", "cavallo": "horse", "elefante": "elephant", "farfalla": "butterfly", "gallina": "chicken", "gatto": "cat", "mucca": "cow", "pecora": "sheep", "scoiattolo": "squirrel", "dog": "cane", "cavallo": "horse", "elephant" : "elefante", "butterfly": "farfalla", "chicken": "gallina", "cat": "gatto", "cow": "mucca", "spider": "ragno", "squirrel": "scoiattolo"

"""# Menghapus Beberapa Folder Label"""

import shutil

useless_folder = ['cane', 'cavallo', 'scoiattolo', 'mucca', 'gatto', 'pecora']

for x in useless_folder:
  path = os.path.join(training_dir, x)
  shutil.rmtree(path)

print(os.listdir(training_dir))

"""# Image Augmentation"""

from tensorflow.keras.preprocessing.image import ImageDataGenerator

training_datagen = ImageDataGenerator(rescale = 1./255,
                                      rotation_range = 20,
                                      zoom_range = 0.2,
                                      shear_range = 0.2,
                                      horizontal_flip = True,
                                      fill_mode = 'nearest',
                                      validation_split = 0.2)

validation_datagen = ImageDataGenerator(rescale = 1./255,
                                        validation_split = 0.2)

training_generator = training_datagen.flow_from_directory(training_dir,
                                                          target_size = (150,150),
                                                          batch_size = 32,
                                                          class_mode = 'categorical',
                                                          subset = 'training')

validation_generator = validation_datagen.flow_from_directory(training_dir,
                                                              target_size = (150,150),
                                                              batch_size = 32,
                                                              class_mode = 'categorical',
                                                              subset = 'validation')

"""# Modelling"""

import tensorflow as tf

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(64, (3,3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(4, activation='softmax')
])

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer=tf.optimizers.Adam(),
              metrics=['accuracy'])

"""# Definisikan Fungsi Callback"""

class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy')>0.92 and logs.get('val_accuracy')>0.92):
      print("\n Model telah mencapai akurasi >92% dan validasi akurasi >92%")
      self.model.stop_training = True

callback_model = myCallback()

"""# Training Model"""

riwayat_training_model = model.fit(training_generator,
                                   epochs=100,
                                   validation_data=validation_generator,
                                   callbacks=[callback_model],
                                   verbose=2)

import matplotlib.pyplot as plt
plt.plot(riwayat_training_model.history['accuracy'])
plt.plot(riwayat_training_model.history['val_accuracy'])
plt.title('Akurasi Model Image Classification')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

import matplotlib.pyplot as plt
plt.plot(riwayat_training_model.history['loss'])
plt.plot(riwayat_training_model.history['val_loss'])
plt.title('Loss Model Image Classification')
plt.ylabel('loss')
plt.xlabel('epoch ke-')
plt.legend(['train', 'test'], loc = 'upper right')
plt.show()

"""# Simpan Model Pada Format SavedModel"""

export_dir = 'saved_model/'
tf.saved_model.save(model, export_dir)

"""# Convert SavedModel Menjadi animal.tflite"""

import pathlib

converter = tf.lite.TFLiteConverter.from_saved_model(export_dir)
tflite_model = converter.convert()

tflite_model_file = pathlib.Path('animal.tflite')
tflite_model_file.write_bytes(tflite_model)

