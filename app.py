from flask import Flask, request, jsonify
import generator


app = Flask(__name__)


@app.route('/')
def generic():
    return jsonify({'сосать'})


@app.route('/generate1')
def generate1():
    namegroup = request.form.get('input')
    size = int(request.form.get('size'))
    limit = int(request.form.get('limit'))

    matrix = generator.builder(namegroup, size, limit)

    return jsonify({'matrix': matrix})


@app.route('/generate2')
def generate2():
    namegroup = request.form.get('input')
    size = int(request.form.get('size'))
    limit = int(request.form.get('limit'))
    task = int(request.form.get('task_number'))

    matrix = generator.builder(namegroup, size, limit, task)

    return jsonify({'matrix': matrix})


