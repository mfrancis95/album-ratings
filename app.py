from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
app.url_map.strict_slashes = False

albums = MongoClient().album_ratings.albums

@app.route('/', methods = ['GET'])
def all():
    return get_albums()

@app.route('/decade/<decade>', methods = ['GET'])
def by_decade(decade):
    try:
        decade = int(decade[:4]) // 10 * 10
        return get_albums({'$and': [{'year': {'$gte': decade}}, {'year': {'$lt': decade + 10}}]})
    except:
        return get_albums()

def get_albums(filters = {}):
    return jsonify(list(albums.find(filters, {'_id': False})))
