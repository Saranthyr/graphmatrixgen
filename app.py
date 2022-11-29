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
    """
        Основной эндпоинт для генерации матрицы
        Аргументы (POST запрос с контентом в формате multipart/form-data):
            namegroup: строка, соответствующая следующему регулярному выражению [А-Яа-я0-9-]+ - в случае несоответствия,
            сервер вернет сообщение в формате application/json:
                {
                    "msg": "incorrect name-group string"
                }
            size: целое число, в случае несоответствия сервер вернет код 500
            negatives: в случае отправки переменной с любым значением, матрица будет содержать отрицательные значения
            graph_type: строка из двух символов, определяющая тип графа - первый символ определяет тип: "o" для ориентированного, "u" для неориентированного, "p" для полновесного;
            второй символ определяет тип значений - "w" для взвешенного и "u" для невзвешенного
    """
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
