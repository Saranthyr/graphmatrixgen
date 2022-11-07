import hashlib
import random


def check_grahp(arr):
    for i in range(len(arr)):
        if arr[i] != 0:
            return False
        else:
            return True


def array_gen_hashlib(size, seed, iteration, matrix):
    arr = []
    seed += hashlib.sha256(bytes(str(iteration), 'utf-8')).hexdigest()
    random.seed(bytes(seed, 'utf-8'))
    zeroes = 100 // random.randint(20, 40)
    for i in range(size):
        number = random.randint(0, 15)
        chance = random.randint(0, 100) % zeroes
        if chance == 0:
            number = 0
        arr.append(number)
    if check_grahp(arr[0:iteration:len(arr)-1]) and arr[iteration] != 0:
        numb = random.randint(0, size-1)
        arr[numb] = random.randint(0, 15)
    return arr


def matrix_checker(matrix, negatives):
    min = 5
    curr_negs = 0
    curr_col = 0
    curr_row = 0
    while curr_negs < negatives and (curr_col != len(matrix)-1 and curr_row != len(matrix)-1):
        for j in range(len(matrix)):
            for k in range(len(matrix)):
                if 0 < matrix[j][k] < min:
                    matrix[j][k] *= -1
                    min = 5
                    curr_negs += 1
                curr_row, curr_col = j, k
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
        matrix = matrix_checker(matrix, negatives)
    return matrix
