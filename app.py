from flask import Flask, request, jsonify
import generator
import flask_cors


app = Flask(__name__)


flask_cors.CORS(app)


@app.route('/')
def generic():
    return jsonify({'сосать'})


@app.route('/generate1', methods=['POST'])
def generate1():
    namegroup = request.form.get('input')
    size = int(request.form.get('size'))
    limit = int(request.form.get('limit'))

    matrix = generator.builder(namegroup, size, limit)

    return jsonify({'matrix': matrix})


@app.route('/generate2', methods=['POST'])
def generate2():
    try:
        namegroup = request.form.get('input')
        size = int(request.form.get('size'))
        limit = int(request.form.get('limit'))
        task = int(request.form.get('task_number'))

        matrix = generator.builder(namegroup, size, limit, task)

        return jsonify({'matrix': matrix})
    except:
        return jsonify({'data': request.data,
                        'formdata': request.form})


