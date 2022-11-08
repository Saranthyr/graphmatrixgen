from flask import Flask, request, jsonify
from flask_cors import cross_origin, CORS

import generator
import re

app = Flask(__name__)


@app.before_request
def activate_cors():
    if request.referrer == 'localhost:3000':
        CORS(app)
        return request
    else:
        return request



@app.route('/')
def generic():
    return jsonify({'hi there'})


@app.route('/generate', methods=['POST'])
def generate_base():
    namegroup = request.form.get('namegroup')
    size = int(request.form.get('size'))
    negatives = request.form.get('negatives', None)
    if re.fullmatch('[А-Яа-я0-9-]+', namegroup):
        if negatives:
            matrix = generator.builder_hashlib(namegroup, size, negatives)
        else:
            matrix = generator.builder_hashlib(namegroup, size)
        return jsonify({'matrix': matrix})
    else:
        return jsonify({'msg': 'incorrect name-group string'})
