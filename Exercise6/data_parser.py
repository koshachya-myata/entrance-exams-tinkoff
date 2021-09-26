from Field import Field
from encryption import decrypt
import os


def load_field(name):
    try:
        f = open(name, 'r')
    except IOError:
        print("Ошибка открытия файла")
        return None
    if os.stat(name).st_size == 0:
        print("Ошибка. Файл пуст")
        return None
    try:
        bombs_enc = list(map(int, next(f).split()))
    except ValueError:
        print("Ошибка чтения файла, данные в файле некорректны")
        return None
    flag = True
    if len(bombs_enc) % 2 == 1:
        print("Ошибка чтения файла, данные в файле некорректны")
        return None
    cols = -1
    user_matrix = []
    flags = []
    i = 1
    while flag:
        s = next(f, 0)
        if s == 0:
            flag = False
            break
        s = s.strip()
        if cols == -1:
            cols = len(s)
        else:
            if cols != len(s):
                break
        j = 1
        lst = []
        for ch in s:
            if ch == 'f':
                flags.append([i, j])
            j += 1
            if ch != 'x' and ch != 'f' and not ch.isdigit():
                flag = False
                break
            else:
                lst.append(ch)
        if flag:
            i += 1
            user_matrix.append(lst)
    f.close()
    rows = len(user_matrix)
    try:
        bombs = decrypt(bombs_enc, rows / 3 + cols / 2 + 1)
    except ValueError:
        print("Ошибка чтения файла, данные в файле некорректны")
        return None
    for x, y in bombs:
        if x <= 0 or x > rows or y <= 0 or y > cols:
            flag = True
            break
    if flag:
        print("Ошибка чтения файла, данные в файле некорректны")
        return None
    return Field(rows, cols, bombs, user_matrix, flags)


def parse_action(user_input, f):
    lst = user_input.strip().split()
    if not lst:
        print("Ошибка: неверный формат данных для действия ({X} {Y} Flag/Open)/(Save {filename})/(Exit)")
        return [0, 0, 0]
    if lst[0].lower() == "exit":
        exit(0)
    if len(lst) == 2 and lst[0].lower() == "save":
        if f.save(lst[1]):
            exit(0)
        return [0, 0, 0]
    size = f.get_size()
    if len(lst) != 3:
        print("Ошибка: неверное количество аргументов")
        return [0, 0, 0]
    if not lst[0].isdigit() or not lst[1].isdigit():
        print("Ошибка: неверный формат данных")
        return [0, 0, 0]
    rows, cols, act = int(lst[0]), int(lst[1]), lst[2].lower()
    if rows < 1 or rows > size[0]:
        print("Ошибка: неверный диапазон для X")
        return [0, 0, 0]
    if cols < 1 or cols > size[1]:
        print("Ошибка: неверный диапазон для Y")
        return [0, 0, 0]
    if act == 'flag':
        act = 1
    elif act == 'open':
        act = 2
    else:
        print("Ошибка: неверный формат данных для действия ({x} {y} Flag/{x} {y} Open/Save {filename}/Exit)")
        return [0, 0, 0]
    return [rows, cols, act]
