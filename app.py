from flask import Flask
from flask import request
import json 
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from flask_cors import CORS, cross_origin
from flask import jsonify

import colorama 
colorama.init()
from colorama import Fore, Style, Back

import random
import pickle

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

with open("intents.json") as file:
    data = json.load(file)

# load trained model
model = keras.models.load_model('chat_model')

# load tokenizer object
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# load label encoder object
with open('label_encoder.pickle', 'rb') as enc:
    lbl_encoder = pickle.load(enc)

@app.route("/chat", methods=['POST'])
def chat():

    content = request.json

    # parameters
    max_len = 20
    
    inp = content["q"]

    result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                            truncating='post', maxlen=max_len))
    tag = lbl_encoder.inverse_transform([np.argmax(result)])

    if tag == ["thanks"] and inp.find("thank") == -1:
     return jsonify({"a":"Sorry I don't understand your question"})

    for i in data['intents']:
        if i['tag'] == tag:
            print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL , np.random.choice(i['responses']))
            return jsonify({"a":np.random.choice(i['responses'])})
