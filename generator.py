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
    while True:
        if zero_count >= 0:
            curr_zero_percentage = zero_count / matrix_size
            if curr_zero_percentage >= zeroes:
                break
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
        if (zero_count + 1)/size > zeroes:
            break
    rows = check_matrix(matrix, size)
    if rows:
        for i in range(len(rows)):
            random.seed(bytes(seed, 'utf-8'))
            y = random.randint(0, size - 1)
            matrix[i][y] = random.randint(1, 15)
    return matrix


def generate_zeroes_unoriented(matrix, seed, size: int):
    random.seed(bytes(str(seed), 'utf-8'))
    zeroes = random.randint(25, 40) / 100
    matrix_size = (size * size - size) / 2
    zero_count = 0
    while True:
        if zero_count >= 0:
            curr_zero_percentage = zero_count / matrix_size
            if curr_zero_percentage >= zeroes:
                break
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
        if (zero_count + 1)/size > zeroes:
            break
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
    sign = False
    while curr_col != len(matrix)-1 and curr_row != len(matrix)-1:
        if sign is False:
            for j in range(len(matrix)):
                if sign is False:
                    for k in range(len(matrix)):
                        if curr_negs < negatives:
                            if 0 < matrix[j][k] < min:
                                matrix[j][k] *= -1
                                min = 5
                                curr_negs += 1
                        else:
                            sign = True
                            break
                        curr_row, curr_col = j, k
                else:
                    break
        else:
            break
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
    points = []
    for i in range(size):
        points.append(i)
    string = hashlib.sha256(bytes(string, 'utf-8')).hexdigest()
    graph_type = list(graph_type)
    if graph_type[0] == 'o':
        for i in range(size):
            seed = hashlib.md5(bytes(string, 'utf-8')).hexdigest()
            matrix.append(array_gen_oriented(size, seed, i))
        matrix = generate_zeroes_oriented(matrix, string, size)
    if graph_type[0] == 'u':
        for i in range(size):
            seed = hashlib.md5(bytes(string, 'utf-8')).hexdigest()
            matrix.append(array_gen_unoriented(size, seed, i, matrix))
        matrix = generate_zeroes_unoriented(matrix, string, size)
    if graph_type[0] == 'p':
        for i in range(size):
            seed = hashlib.md5(bytes(string, 'utf-8')).hexdigest()
            matrix.append(array_gen_unoriented(size, seed, i, matrix))

    if graph_type[0] in ['o', 'u'] and negatives:
        random.seed(string)
        negatives = random.randint(2, 5)
        print(negatives)
        matrix = matrix_checker(matrix, negatives)

    if graph_type[1] == 'u' and matrix != []:
        matrix = unweighted_convert(matrix)

    return matrix
