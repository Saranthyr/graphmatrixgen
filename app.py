from flask import Flask, request, jsonify
import flask_sqlalchemy
from sqlalchemy import MetaData

import generator
import flask_cors
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'mysql+pymysql://std_1875_graphmatrixgen:Vjt_gjxntybt1@std-mysql/std_1875_graphmatrixgen?charset=utf8'
app.config['NAMING_CONVENTION'] = {
    'pk': 'pk_%(table_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'ix': 'ix_%(table_name)s_%(column_0_name)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
}
db = flask_sqlalchemy.SQLAlchemy(app, metadata=MetaData(naming_convention=app.config['NAMING_CONVENTION']))

flask_cors.CORS(app)


@app.route('/')
def generic():
    return jsonify({'hi there'})


@app.route('/generate_without_task_number', methods=['POST'])
def generate_base():
    namegroup = request.form.get('namegroup')
    size = int(request.form.get('size'))
    limit = int(request.form.get('limit'))
    if re.fullmatch('[А-Яа-я0-9-]+', namegroup):
        matrix = generator.builder_hashlib(namegroup, size, limit)
        return jsonify({'matrix': matrix})
    else:
        return jsonify({'msg': 'incorrect name-group string'})


@app.route('/generate_with_task_number', methods=['POST'])
def generate_advanced():
    namegroup = request.form.get('namegroup')
    size = int(request.form.get('size'))
    limit = int(request.form.get('limit'))
    task = int(request.form.get('task_number'))
    print(request.headers)
    if re.fullmatch('[А-Яа-я0-9-]+', namegroup):
        matrix = generator.builder_hashlib(namegroup, size, limit, task)
        return jsonify({'matrix': matrix})
    else:
        return jsonify({'msg': 'incorrect name-group string'})


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
