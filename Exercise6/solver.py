from Field import Field

from lib import *
from random import randint


def set_group(coords, matrix):
    """
    Возвращает кол-во бомб в этой ячейке и координаты неоткрытых ячеек вокруг.
    """
    rt = []
    x = coords[0]
    y = coords[1]
    if not matrix[x][y].isdigit():
        return None
    rt.append(ord(matrix[x][y]) - ord('0'))
    group = []
    for i in range(x - 1, x + 2):
        if i < 0 or i >= len(matrix):
            continue
        for j in range(y - 1, y + 2):
            if j < 0 or j >= len(matrix[0]) or matrix[i][j].isdigit():
                continue
            group.append([i, j])
    group.sort()
    if len(group) == 0:
        return None
    rt.append(group)
    return rt


def contains_group(a, b):
    for el in b:
        if el not in a:
            return False
    return True


def group_substract(b, s):
    rt = []
    groups = list_substract(b[1], s[1])
    rt.append(b[0] - s[0])
    rt.append(groups)
    return rt


def list_substract(b, s):
    rt = []
    for i in range(len(b)):
        if b[i] not in s:
            rt.append(b[i])
    return rt


def intersect_lists(b, s):
    rt = []
    for el in s:
        if el in b:
            rt.append(el)
    return rt


def intersect_groups(b, s):
    overlap = intersect_lists(b[1], s[1])
    bombs = b[0] - len(list_substract(s[1], overlap))
    overlap_group = [bombs, overlap]
    if bombs != s[0]:
        return None
    return overlap_group


def create_cells_groups(field: Field):
    """
    Соеденим ячейки в группы. Уберем повторяющиеся, разъеденим пересекающеся
    """
    matrix = field.get_field()
    groups = []
    for x in range(field.get_size()[0]):
        for y in range(field.get_size()[1]):
            gr = set_group([x, y], matrix)
            if gr is not None:
                groups.append(gr)
    repeat = True
    while repeat:
        repeat = False
        for i in range(len(groups)):
            j = i + 1
            while j < len(groups):
                if groups[i] == groups[j]:
                    groups.pop(j)
                    break
                bigger = []
                smaller = []
                if len(groups[i][1]) > len(groups[j][1]):
                    bigger = groups[i]
                    bigger_index = i
                    smaller = groups[j]
                else:
                    bigger = groups[j]
                    bigger_index = j
                    smaller = groups[i]
                if contains_group(bigger[1], smaller[1]):
                    groups[bigger_index] = group_substract(bigger, smaller)
                    if len(groups[bigger_index][1]) == 0:
                        groups.pop(bigger_index)
                        j -= 1
                    repeat = True
                elif len(intersect_lists(groups[i][1], groups[j][1])) > 0:
                    if groups[i][0] > groups[j][0]:
                        bigger = groups[i]
                        bigger_index = i
                        smaller = groups[j]
                    else:
                        bigger = groups[j]
                        bigger_index = j
                        smaller = groups[i]
                    intersected = intersect_groups(bigger, smaller)
                    if intersected is not None:
                        groups.append(intersected)
                        groups[bigger_index] = group_substract(bigger, intersected)
                        groups[i + j - bigger_index] = group_substract(smaller, intersected)
                        if len(groups[i + j - bigger_index]) == 0:
                            groups.pop(i + j - bigger_index)
                            j -= 1
                        repeat = True
                j += 1
    return groups


def bot_win(field):
    field.print_field()
    print("Бот победил!")
    exit(0)


def bot_dead(field):
    field.print_field()
    print("Бот проиграл(!")
    exit(0)


def open_all(field: Field):
    """
    Открывает все оставшиеся ячейки
    (используется после того, как бот использовал все флажки).
    """
    matrix = field.get_field()
    r, c = field.get_size()
    for i in range(r):
        for j in range(c):
            if matrix[i][j] == 'x':
                if not field.open(i + 1, j + 1):
                    bot_dead(field)


def open_random(field):
    matrix = field.get_field()
    r, c = field.get_size()
    closed = []
    for i in range(r):
        for j in range(c):
            if matrix[i][j] == 'x':
                closed.append([i + 1, j + 1])
    choice = closed[randint(0, len(closed) - 1)]
    is_alive = field.open(choice[0], choice[1])
    if not is_alive:
        print(choice)
        bot_dead(field)
    return field


def action_groups(groups, field: Field):
    """
    Открывает ячейки, в которых точно нет бомб.
    Помечает флажками ячейки, в которых точно есть бомба.
    Если ничего не открылось, открывает случайню ячейку.
    """
    is_any_open = False
    for gr in groups:
        if gr[0] == 0:
            for n in gr[1]:
                if field.get_field()[n[0]][n[1]] == 'x':
                    is_any_open = True
                    if not field.open(n[0] + 1, n[1] + 1):
                        bot_dead(field)

        if len(gr[1]) == gr[0]:
            for n in gr[1]:
                if field.get_field()[n[0]][n[1]] != 'f':
                    field.change_flag(n[0] + 1, n[1] + 1)
                if field.get_flags_count() == field.get_bombs_count():
                    is_any_open = True
                    open_all(field)
                    if field.is_win():
                        field.print_field()
                        bot_win(field)
    if not is_any_open:
        return open_random(field)
    return field


def solve(field: Field):
    field.clear_flags()
    x = field.get_size()[0]
    y = field.get_size()[1]
    field.print_field()
    first = field.open(randint(1, x), randint(1, y))
    if not first:
        field.print_field()
        print("Бот проиграл при первом открытии ячейки :(((")
        exit(0)
    while True:
        field.print_field()
        groups = create_cells_groups(field)
        field = action_groups(groups, field)
