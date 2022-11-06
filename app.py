from flask import Flask, request, jsonify

import generator
import re

app = Flask(__name__)


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
