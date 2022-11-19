from flask import Flask, request, jsonify
from flask_cors import cross_origin, CORS

import generator
import re

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])


@app.route('/')
def generic():
    return jsonify({'hi there'})


@app.route('/generate', methods=['POST'])
def generate_base():
    namegroup = request.form.get('namegroup')
    size = int(request.form.get('size'))
    negatives = request.form.get('negatives', None)
    graph_type = request.form.get('graph_type')
    if re.fullmatch('[А-Яа-я0-9-]+', namegroup):
        if negatives:
            matrix = generator.builder_hashlib(namegroup, size, graph_type, negatives)
        else:
            matrix = generator.builder_hashlib(namegroup, size, graph_type)
        return jsonify({'matrix': matrix})
    else:
        return jsonify({'msg': 'incorrect name-group string'})
