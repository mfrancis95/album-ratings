from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
app.url_map.strict_slashes = False

albums = MongoClient().album_ratings.albums
insert_keys = ['artist', 'rating', 'score', 'score_max', 'title', 'year']

@app.route('/')
def all():
    return get_albums()

@app.route('/decade/<decade>')
def by_decade(decade):
    try:
        decade = int(decade[:4]) // 10 * 10
        return get_albums({'$and': [{'year': {'$gte': decade}}, {'year': {'$lt': decade + 10}}]})
    except:
        return get_albums()

def get_albums(filters = {}):
    return jsonify(list(albums.find(filters, {'_id': False})))

@app.route('/insert', methods = ['POST'])
def insert():
    try:
        json = request.get_json()
        json['rating'] = json['score'] / json['score_max']
        albums.insert({key: json[key] for key in insert_keys})
    except:
        pass
    return ''
