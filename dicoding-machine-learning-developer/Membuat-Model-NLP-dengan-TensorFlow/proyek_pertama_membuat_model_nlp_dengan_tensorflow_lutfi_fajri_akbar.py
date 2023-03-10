# -*- coding: utf-8 -*-
"""Proyek Pertama : Membuat Model NLP dengan TensorFlow_Lutfi Fajri Akbar.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uI485HnVN4aZLryUxT4-WCTT7CBDQ19i

# Proyek Pertama Klasifikasi Gender Berdasarkan Namanya

# Data Diri
### **Nama** : 
Lutfi Fajri Akbar
### **No. Register** :
1494037162101-2551
### **Username Dicoding**:
lutfifajri02
### **E-mail**:
ltfffajri@gmail.com

# Codelab
"""

import pandas as pd
df = pd.read_csv('/content/indonesian-names-people.csv')

df.info()

df.head(10)

df['gender'].replace(['m', 'f'], [0,1], inplace=True)
df.head(20)

nama_orang = df['name'].values
label = df['gender'].values

nama_orang

label

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(nama_orang, label, test_size=0.2)

len(x_train)

len(x_test)

from tensorflow.keras.preprocessing.text import Tokenizer

tokenizer = Tokenizer(num_words = 5000, oov_token = 'x')
tokenizer.fit_on_texts(x_train)

word_index = tokenizer.word_index
print(word_index)

sequence_train = tokenizer.texts_to_sequences(x_train)
sequence_test = tokenizer.texts_to_sequences(x_test)

from tensorflow.keras.preprocessing.sequence import pad_sequences

padded_train = pad_sequences(sequence_train,
                             padding='post',
                             maxlen=4,
                             truncating='post')

padded_test = pad_sequences(sequence_test,
                            padding='post',
                            maxlen=4,
                            truncating='post')

import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=5000, output_dim=32),
    tf.keras.layers.LSTM(64),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.summary()

model.compile(loss='binary_crossentropy',
              optimizer='Adam',
              metrics=['accuracy'])

import tensorflow as tf

class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy')>0.99):
      print("\nAkurasi model telah mencapai >99%")
      self.model.stop_training = True

callback_model = myCallback()

riwayat_model = model.fit(padded_train, y_train,
                          epochs = 10,
                          validation_data = (padded_test, y_test),
                          callbacks=[callback_model],
                          verbose=2)

# Membuat plot akurasi dari model

import matplotlib.pyplot as plt

plt.plot(riwayat_model.history['accuracy'])
plt.plot(riwayat_model.history['val_accuracy'])
plt.title('Akurasi Model')
plt.ylabel('accuracy')
plt.xlabel('epoch ke-')
plt.legend(['train', 'test'], loc = 'lower right')
plt.show()

# Membuat plot loss dari model

import matplotlib.pyplot as plt

plt.plot(riwayat_model.history['loss'])
plt.plot(riwayat_model.history['val_loss'])
plt.title('Loss Model')
plt.ylabel('loss')
plt.xlabel('epoch ke-')
plt.legend(['train', 'test'], loc = 'upper right')
plt.show()

