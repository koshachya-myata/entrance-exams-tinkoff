import random


def intersect_lists(b, s):
    rt = []
    for el in s:
        if el in b:
            rt.append(el)
    return rt


def list_substract(b, s):
    rt = []
    for i in range(len(b)):
        if b[i] not in s:
            rt.append(b[i])
    return rt


def is_matrix_only_form_chr(m, c):
    for row in m:
        for el in row:
            if el != c:
                return False
    return True


def error():
    print("Ошибка валидации введенных данных.")


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
