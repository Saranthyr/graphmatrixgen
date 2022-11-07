import hashlib
import random


def check_grahp(arr):
    for i in range(len(arr)):
        if arr[i] != 0:
            return False
        else:
            return True


def generate_zeroes(matrix, seed, size: int):
    random.seed(bytes(str(seed) , 'utf-8'))
    zeroes = 100 // random.randint(20, 40)
    matrix_size = size*size
    percentage = matrix_size//zeroes
    zero_count = 0
    while zero_count < percentage:
        seed_zeroes = hashlib.sha1(bytes(str(seed) + str(zero_count), 'utf-8')).hexdigest()
        random.seed(bytes(str(seed_zeroes), 'utf-8'))
        i = random.randint(0, size)
        j = random.randint(0, size)
        if matrix[i][j] == 0:
            continue
        else:
            matrix[i][j] = 0
    return matrix


def array_gen_hashlib(size, seed, iteration):
    arr = []
    seed += hashlib.sha256(bytes(str(iteration), 'utf-8')).hexdigest()
    random.seed(bytes(seed, 'utf-8'))
    for i in range(size):
        number = random.randint(0, 15)
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
        seed = hashlib.md5(bytes(string, 'utf-8')).hexdigest()
        matrix.append(array_gen_hashlib(size, seed, i))
    generate_zeroes(matrix, size, string)
    if negatives:
        random.seed(string)
        negatives = random.randint(2, 5)
        matrix = matrix_checker(matrix, negatives)
    return matrix
