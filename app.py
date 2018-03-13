from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
app.url_map.strict_slashes = False

albums = MongoClient().album_ratings.albums

@app.route('/', methods = ['GET'])
def all():
    return jsonify(list(albums.find({}, {'_id': False})))
