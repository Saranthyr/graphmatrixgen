from flask import Flask, request, jsonify
import flask_sqlalchemy
import generator
import flask_cors
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'mysql+mysqlconnector://std_1875_graphmatrixgen:Vjt_gjxntybt1!@std-mysql/std_1875_graphmatrixgen'
db = flask_sqlalchemy.SQLAlchemy(app)

flask_cors.CORS(app)


@app.route('/')
def generic():
    return jsonify({'hi there'})


@app.route('/generate_without_task_number', methods=['POST'])
def generate_base():
    namegroup = request.form.get('input')
    size = int(request.form.get('size'))
    limit = int(request.form.get('limit'))

    matrix = generator.builder_hashlib(namegroup, size, limit)

    return jsonify({'matrix': matrix})


@app.route('/generate_with_task_number', methods=['POST'])
def generate_advanced():
    namegroup = request.form.get('namegroup')
    size = int(request.form.get('size'))
    limit = int(request.form.get('limit'))
    task = int(request.form.get('task_number'))

    matrix = generator.builder_hashlib(namegroup, size, limit, task)

    return jsonify({'matrix': matrix})


@app.route('/generate_with_saving_into_db', methods=['POST'])
def generate_db():
    namegroup = request.form.get('namegroup')
    size = int(request.form.get('size'))
    limit = int(request.form.get('limit'))
    if re.fullmatch('[А-Яа-я0-9-]+', namegroup):
        matrix = generator.builder_werkzeug(namegroup, size, limit)
        return jsonify({'matrix': matrix})
    else:
        return jsonify({'msg': 'incorrect name-group string'})
