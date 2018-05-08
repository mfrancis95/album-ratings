from pymongo import MongoClient
from flask import request

albums = MongoClient().album_ratings.albums
keys = ['artist', 'own', 'rating', 'score', 'score_max', 'title', 'year']
key_types = {
    'artist': str,
    'score': int,
    'score_max': int,
    'title': str,
    'year': int
}

def boolean(value):
    return value != 'false' if value is not None else False

def create_filters(filters = {}):
    try:
        filters['year'] = int(request.args['year'])
    except:
        pass
    return filters

def get_count():
    return albums.count(create_filters())

def get_albums():
    return list(albums.find(create_filters(), {'_id': False}))

def get_albums_by_decade(decade):
    return list(albums.find(create_filters({'$and': [{'year': {'$gte': decade}}, {'year': {'$lt': decade + 10}}]}), {'_id': False}))

def insert_album():
    try:
        album = request.form.to_dict() or request.get_json(True)
        for key, func in key_types.items():
            album[key] = func(album[key])
        album['own'] = boolean(album.get('own'))
        album['rating'] = album['score'] / album['score_max']
        albums.insert({key: album[key] for key in keys})
        return True
    except:
        return False