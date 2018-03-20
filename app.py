from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
app.url_map.strict_slashes = False

albums = MongoClient().album_ratings.albums
keys = ['artist', 'rating', 'score', 'score_max', 'title', 'year']
key_types = {
    'artist': str,
    'score': int,
    'score_max': int,
    'title': str,
    'year': int
}

@app.route('/')
def all():
    return get_albums()

@app.route('/decade/<decade>')
def by_decade(decade):
    try:
        decade = int(decade[:4]) // 10 * 10
        return get_albums(filters = {'$and': [{'year': {'$gte': decade}}, {'year': {'$lt': decade + 10}}]})
    except:
        return get_albums()

@app.route('/count')
def count():
    return get_albums(True)

def get_albums(count = False, filters = {}):
    if count:
        return jsonify(albums.count(filters))
    return jsonify(list(albums.find(filters, {'_id': False})))

@app.route('/insert', methods = ['POST'])
def insert():
    try:
        album = request.form.to_dict() or request.get_json(True)
        for key, func in key_types.items():
            album[key] = func(album[key])
        album['rating'] = album['score'] / album['score_max']
        albums.insert({key: album[key] for key in keys})
    except:
        pass
    return ''