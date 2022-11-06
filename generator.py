import hashlib
import random


def array_gen_hashlib(size, seed, iteration, matrix):
    arr = []
    seed += hashlib.sha256(bytes(str(iteration), 'utf-8')).hexdigest()
    random.seed(bytes(seed, 'utf-8'))
    zeroes = 100 // random.randint(15, 25)
    for i in range(size):
        if matrix:
            if i < iteration:
                number = matrix[i][iteration]
            else:
                number = random.randint(0, 20)
                chance = random.randint(0, 100) % zeroes
                if chance == 0:
                    number = 0
        else:
            number = random.randint(0, 20)
            chance = random.randint(0, 100) % zeroes
            if chance == 0:
                number = 0
        arr.append(number)
    return arr


def matrix_checker(matrix, negatives):
    min = 5
    curr_negs = 0
    while curr_negs < negatives:
        for j in range(len(matrix)):
            for k in range(len(matrix)):
                if 0 < matrix[j][k] < min:
                    matrix[j][k] *= -1
                    matrix[k][j] *= -1
                    min = 5
                    curr_negs += 1
    return matrix


def builder_hashlib(string, size: int, negatives=None):
    matrix = []
    string += str(size)
    string = hashlib.sha256(bytes(string, 'utf-8')).hexdigest()
    for i in range(size):
        seed = hashlib.sha256(bytes(string, 'utf-8')).hexdigest()
        matrix.append(array_gen_hashlib(size, seed, i, matrix))
    if negatives:
        random.seed(string)
        negatives = random.randint(2, 5)
        print(negatives)
        matrix = matrix_checker(matrix, negatives)
    return matrix
