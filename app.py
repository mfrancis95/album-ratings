from flask import Flask, jsonify
from .database import get_albums, get_albums_by_decade, get_count, insert_album

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/')
def all():
    return jsonify(get_albums())

@app.route('/decade/<decade>')
def by_decade(decade):
    try:
        decade = int(decade[:4]) // 10 * 10
        return jsonify(get_albums_by_decade(decade))
    except:
        return jsonify(get_albums())

@app.route('/count')
def count():
    return get_count()

@app.route('/insert', methods = ['POST'])
def insert():
    insert_album()
    return ''