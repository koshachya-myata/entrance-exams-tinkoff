import random


def is_in_range(x, start, end):
    if x < start or x > end:
        return 0
    return 1


def get_matrix(rows, cols, bombs):
    matrix = []
    for i in range(rows):
        matrix.append([0] * cols)
    for x, y in bombs:
        for i in range(x-2, x + 1):
            for j in range(y-2, y+1):
                if is_in_range(i, 0, rows - 1) and is_in_range(j, 0, cols - 1) and [i + 1, j + 1] != [x, y]:
                    matrix[i][j] += 1
    return matrix


def get_bombs(n, m, count):
    rt = []
    i = 0
    while i < count:
        x = random.randint(1, n)
        y = random.randint(1, m)
        if [x, y] not in rt:
            rt.append([x, y])
            i += 1
    return rt
