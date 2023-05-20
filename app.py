import configparser
import os
import bson
from flask import Flask, current_app, g, jsonify, request
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo

from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))

app = Flask(__name__)
app.debug = True
app.config['MONGO_URI'] = config['PROD']['DB_URI']

chatbot = ChatBot("Ron Obvious")

conversation = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome."
]

trainer = ListTrainer(chatbot)

trainer.train(conversation) 

def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:

        db = g._database = PyMongo(current_app).db
       
    return db

# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def response(user_response):
    robo_response=''
    if(user_response):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = "test"
        return robo_response

@app.route("/chat", methods=['POST'])
def chat():
    data = request.get_json()
    # return jsonify(data)
    user_response = data['q']
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            return jsonify({'a':"ROBO: You are welcome.."})
        else:
            print("ROBO: ",end="")
            print(response(user_response))
            botResponse = chatbot.get_response(user_response)
            print(botResponse)
            return jsonify({'a':str(botResponse)})
    else:
        flag=False
        return jsonify({'a':"ROBO: Bye! take care.."}) 
    
@app.route("/testdb", methods=['POST'])
def add_comment():
    data = request.get_json()
    movie_id = data['movie_id']
    name = data['name']
    email = data['email']
    comment = data['comment']
    date = data['date']
    """
    Inserts a comment into the comments collection, with the following fields:

    - "name"
    - "email"
    - "movie_id"
    - "text"
    - "date"

    Name and email must be retrieved from the "user" object.
    """

    comment_doc = { 'movie_id' : movie_id, 'name' : name, 'email' : email,'text' : comment, 'date' : date}
    db.comments.insert_one(comment_doc)
    return jsonify({'a':"data added"}) 