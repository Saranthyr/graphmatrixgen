import hashlib
import random
import uuid

from sqlalchemy import and_
from werkzeug.security import generate_password_hash
from models import Students, MatrixParams


def array_gen_hashlib(size, seed, limit, iteration):
    arr = []
    seed += hashlib.sha256(bytes(str(iteration), 'utf-8')).hexdigest()
    random.seed(bytes(seed, 'utf-8'))
    zeroes = 100 // random.randint(25, 50)
    for i in range(size):
        number = random.randint(-limit, limit)
        chance = random.randint(0, 100) % zeroes
        if chance == 0:
            number = 0
        arr.append(number)
    return arr


def builder_hashlib(string, size: int, limit: int, task_number=None):
    matrix = []
    string += str(limit) + str(size)
    if task_number:
        string += str(task_number)
    for i in range(size):
        seed = hashlib.sha256(bytes(string, 'utf-8')).hexdigest()
        matrix.append(array_gen_hashlib(size, seed, limit, i))
    return matrix


def array_gen_werkzeug(size, seed, limit):
    arr = []
    random.seed(bytes(seed, 'utf-8'))
    zeroes = 100 // random.randint(10, 40)
    for i in range(size):
        number = random.randint(-limit, limit)
        chance = random.randint(0, 100) % zeroes
        if chance == 0:
            number = 0
        arr.append(number)
    return arr


def builder_werkzeug(string, size: int, limit: int):
    from app import db
    matrix = []
    student = db.session.query(Students).filter(Students.student_name_group.ilike(string)).one_or_none()
    if student:
        student_matrix_params = db.session.query(MatrixParams).filter(and_(MatrixParams.student_id == student.id,
                                                                           MatrixParams.size == size)).one_or_none()
        if student_matrix_params:
            size = student_matrix_params.size
            limit = student_matrix_params.matrix_limit
            seeds = student_matrix_params.seeds.split(';')
            for i in range(len(seeds)):
                matrix.append(array_gen_werkzeug(size, seeds[i], limit))
        else:
            seeds = ''
            for i in range(size):
                seed = generate_password_hash(string, 'sha256', 64)
                seeds += seed + ';'
                matrix.append(array_gen_werkzeug(size, seed, limit))
            matrix_params = MatrixParams(
                id=str(uuid.uuid4()),
                student_id=student.id,
                size=size,
                matrix_limit=limit,
                seeds=seeds
            )
            db.session.add(matrix_params)
            db.session.flush()
            db.session.commit()
    else:
        stud_id = str(uuid.uuid4())
        student = Students(
            id=stud_id,
            student_name_group=string
        )
        db.session.add(student)
        seeds = ''
        for i in range(size):
            seed = generate_password_hash(string, 'sha256', 64)
            seeds += seed + ';'
            matrix.append(array_gen_werkzeug(size, seed, limit))
        matrix_params = MatrixParams(
            id=str(uuid.uuid4()),
            student_id=stud_id,
            size=size,
            matrix_limit=limit,
            seeds=seeds
        )
        db.session.add(matrix_params)
        db.session.flush()
        db.session.commit()
    return matrix
