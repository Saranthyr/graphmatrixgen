import hashlib
import random


def array_gen(size, seed, limit, iteration):
    arr = []
    if iteration is not None:
        seed += hashlib.sha256(bytes(str(iteration), 'utf-8')).hexdigest()
    random.seed(bytes(seed, 'utf-8'))
    zeroes = 100 // random.randint(10, 40)
    for i in range(size):
        number = random.randint(-limit, limit)
        chance = random.randint(0, 100) % zeroes
        if chance == 0:
            number = 0
        arr.append(number)
    return arr


def builder(string, size: int, limit: int, task_number = None):
    matrix = []
    string += str(limit) + str(size)
    if task_number:
        string += str(task_number)
    for i in range(size):
        seed = hashlib.sha256(bytes(string, 'utf-8')).hexdigest()
        matrix.append(array_gen(size, seed, limit, i))
    return matrix
