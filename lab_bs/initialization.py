# by Nam Hoang
# so codv

import numpy as np
from nltk.tokenize import RegexpTokenizer
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers.core import Dense, Activation
from keras.optimizers import RMSprop
import pickle
import keras
import os
from pyvi import ViTokenizer


WORD_LENGTH = 2


file_list = []
for (dirpath, dirname, filename) in os.walk('Train_Full'):
    for f in filename:
        file_list.append(dirpath+'/'+f)

sequences = ""
for f in file_list:
    with open(f,encoding="utf-16", errors='ignore') as x:
        text = x.read().lower()
        sequences+=" "+text

text = ViTokenizer.tokenize(sequences)
tokenizer = RegexpTokenizer(r'\w+')
words = tokenizer.tokenize(text)

tokenizer = keras.preprocessing.text.Tokenizer(filters='!"#$%&()*+,-./:;<=>?@[\]^`{|}~ ')
tokenizer.fit_on_texts(words)

unique_word_index = tokenizer.word_index
unique_words = len(tokenizer.word_index)

prev_words = []
next_words = []
for i in range(len(words) - WORD_LENGTH):
    prev_words.append(words[i:i + WORD_LENGTH])
    next_words.append(words[i + WORD_LENGTH])
print(prev_words[0], next_words[0])
print(prev_words[1], next_words[1])
X = np.zeros((len(prev_words), WORD_LENGTH, unique_words), dtype=bool)
Y = np.zeros((len(next_words), unique_words), dtype=bool)
for i, each_words in enumerate(prev_words):
    for j, each_word in enumerate(each_words):
        X[i, j, unique_word_index[each_word]-1] = 1
    Y[i, unique_word_index[next_words[i]]-1] = 1

model = Sequential()
model.add(LSTM(128, input_shape=(WORD_LENGTH, unique_words)))
model.add(Dense(unique_words))
model.add(Activation('softmax'))
optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
history = model.fit(X, Y, validation_split=0.05, batch_size=1000, epochs=15, shuffle=True).history

model.save('keras_next_word_model.h5')
pickle.dump(history, open("history.p", "wb"))
with open('tokenizer.pkl', 'wb') as f:
    pickle.dump(tokenizer, f)
