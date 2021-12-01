# by Nam Hoang
# so codv

import numpy as np
from nltk.tokenize import RegexpTokenizer
from keras.models import load_model
import pickle
import heapq
from pyvi import ViTokenizer

WORD_LENGTH = 2


model = load_model('keras_next_word_model.h5')
history = pickle.load(open("history.p", "rb"))
with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

unique_word_index = tokenizer.word_index
unique_words = len(unique_word_index)
indices_char = list(unique_word_index.keys())


def prepare_input(text):
    x = np.zeros((1, WORD_LENGTH, unique_words))
    text = ViTokenizer.tokenize(text)
    tokenizers = RegexpTokenizer(r'\w+')
    words = tokenizers.tokenize(text)
    words = words[-WORD_LENGTH:]
    for t, word in enumerate(words):
        print(word, end=" ")
        x[0, t, unique_word_index[word]-1] = 1
    return x


def predict_completion(text):
    original_text = text
    completion = ''
    while True:
        x = prepare_input(text)
        preds = model.predict(x, verbose=0)[0]
        next_index = sample(preds, top_n=1)[0]
        next_char = tokenizer.word_index[next_index+1]
        text = text[1:] + next_char
        completion += next_char
        if len(original_text + completion) + 2 > len(original_text) and next_char == ' ':
            return completion


def predict_completions(text, n=3):
    x = prepare_input(text)
    preds = model.predict(x, verbose=0)[0]
    next_indices = sample(preds, n)
    return [indices_char[idx] for idx in next_indices]


def sample(preds, top_n=3):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds)
    return heapq.nlargest(top_n, range(len(preds)), preds.take)

print("dự đoán từ tiếp theo:")
# print(predict_completions("trong khi".lower(), 2))
while(True):
    value= input("nhập 1 vài từ: ")
    print(predict_completions(value.lower(), 2))