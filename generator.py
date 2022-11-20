import hashlib
import random


def check_matrix(matrix, size):
    zero_row = []
    for i in range(size):
        if all(v == 0 for v in matrix[i]):
            zero_row.append(i)
    if len(zero_row) > 0:
        return zero_row


def generate_zeroes_oriented(matrix, seed, size: int):
    random.seed(bytes(str(seed), 'utf-8'))
    zeroes = random.randint(25, 40) / 100
    matrix_size = size * size
    zero_count = 0
    curr_zero_percentage = 0
    while curr_zero_percentage < zeroes:
        if zero_count > 0:
            curr_zero_percentage = zero_count / matrix_size
        seed_zeroes = hashlib.sha1(bytes(str(seed) + str(zero_count), 'utf-8')).hexdigest()
        random.seed(bytes(str(seed_zeroes), 'utf-8'))
        i = random.randint(0, size-1)
        j = random.randint(0, size-1)
        curr_num = matrix[i][j]
        while curr_num == 0:
            i = random.randint(0, size-1)
            j = random.randint(0, size-1)
            curr_num = matrix[i][j]
        else:
            matrix[i][j] = 0
            zero_count += 1
    return matrix


def generate_zeroes_unoriented(matrix, seed, size: int):
    random.seed(bytes(str(seed), 'utf-8'))
    zeroes = random.randint(25, 40) / 100
    matrix_size = (size * size - size) / 2
    zero_count = 0
    curr_zero_percentage = 0
    print(zeroes)
    while curr_zero_percentage < zeroes:
        if zero_count > 0:
            curr_zero_percentage = zero_count / matrix_size
        seed_zeroes = hashlib.sha1(bytes(str(seed) + str(zero_count), 'utf-8')).hexdigest()
        random.seed(bytes(str(seed_zeroes), 'utf-8'))
        i = random.randint(0, size - 1)
        j = random.randint(0, size - 1)
        curr_num = matrix[i][j]
        while curr_num == 0:
            i = random.randint(0, size-1)
            j = random.randint(0, size-1)
            curr_num = matrix[i][j]
        else:
            matrix[i][j] = 0
            matrix[j][i] = 0
            zero_count += 1
    rows = check_matrix(matrix, size)
    if rows:
        for i in range(len(rows)):
            random.seed(bytes(seed, 'utf-8'))
            y = random.randint(0, size-1)
            if y == i:
                y = random.randint(0, size - 1)
            matrix[i][y] = random.randint(1, 15)
            matrix[y][i] = matrix[i][y]
    return matrix


def array_gen_oriented(size, seed, iteration):
    arr = []
    seed += hashlib.sha256(bytes(str(iteration), 'utf-8')).hexdigest()
    random.seed(bytes(seed, 'utf-8'))
    for i in range(size):
        number = random.randint(1, 15)
        arr.append(number)
    return arr


def array_gen_unoriented(size, seed, iteration, matrix):
    arr = []
    seed += hashlib.sha256(bytes(str(iteration), 'utf-8')).hexdigest()
    random.seed(bytes(seed, 'utf-8'))
    for i in range(size):
        number = random.randint(1, 15)
        if matrix:
            if i < iteration:
                number = matrix[i][iteration]
        if iteration == i:
            number = 0
        arr.append(number)
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


def unweighted_convert(matrix):
    s = len(matrix)
    matrix = matrix
    for i in range(s):
        for j in range(s):
            if matrix[i][j] > 0:
                matrix[i][j] = 1
    return matrix


def builder_hashlib(string, size: int, graph_type: str, negatives=None):
    matrix = []
    string += str(size)
    string = hashlib.sha256(bytes(string, 'utf-8')).hexdigest()
    if graph_type == 'ow':
        for i in range(size):
            seed = hashlib.md5(bytes(string, 'utf-8')).hexdigest()
            matrix.append(array_gen_oriented(size, seed, i))
        generate_zeroes_oriented(matrix, string, size)
        if negatives:
            random.seed(string)
            negatives = random.randint(2, 5)
            matrix = matrix_checker(matrix, negatives)
    if graph_type == 'uw':
        for i in range(size):
            seed = hashlib.md5(bytes(string, 'utf-8')).hexdigest()
            matrix.append(array_gen_unoriented(size, seed, i, matrix))
        generate_zeroes_unoriented(matrix, string, size)
        if negatives:
            random.seed(string)
            negatives = random.randint(2, 5)
            matrix = matrix_checker(matrix, negatives)
    if graph_type == 'ou':
        for i in range(size):
            seed = hashlib.md5(bytes(string, 'utf-8')).hexdigest()
            matrix.append(array_gen_oriented(size, seed, i))
        generate_zeroes_oriented(matrix, string, size)
        unweighted_convert(matrix)
    if graph_type == 'uu':
        for i in range(size):
            seed = hashlib.md5(bytes(string, 'utf-8')).hexdigest()
            matrix.append(array_gen_unoriented(size, seed, i, matrix))
        generate_zeroes_unoriented(matrix, string, size)
        unweighted_convert(matrix)
    if graph_type == 'pu':
        for i in range(size):
            seed = hashlib.md5(bytes(string, 'utf-8')).hexdigest()
            matrix.append(array_gen_unoriented(size, seed, i, matrix))
        unweighted_convert(matrix)
    if graph_type == 'pw':
        for i in range(size):
            seed = hashlib.md5(bytes(string, 'utf-8')).hexdigest()
            matrix.append(array_gen_unoriented(size, seed, i, matrix))
    return matrix
