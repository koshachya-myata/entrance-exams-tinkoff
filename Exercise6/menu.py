from Field import Field
from lib import *
from data_parser import load_field
from solver import solve


HELLO = "Привет!\nЧтобы начать новую игру напиши start\n"\
        "Чтобы загрузить старую игру напиши load {filename}\nЧтобы играл бот, напиши bot"


def get_num(text):
    if text.lower() == "exit":
        exit(0)
    flag = True
    rt = 0
    while flag:
        print(text)
        rt_str = input().strip()
        if not rt_str.isdigit():
            error()
        else:
            rt = int(rt_str)
            flag = False
    return rt


def bot():
    print("Напишите load {filename}, если хотите, чтобы бот решал сохраненную карту")
    print("Напишите start, если хотите, сгенерировать карту для бота")
    while True:
        s = input().strip()
        if s.lower() == "exit":
            exit(0)
        if s.lower() == "start":
            f = start()
            break
        elif len(s.split()) == 2 and s.split()[0].lower() == "load":
            f = load_field(s.split()[1])
            if f is None:
                print("Введите start/load {filename}/exit")
                continue
            break
        else:
            print("Ошибка. Введите start/load {filename}/exit")
    solve(f)


def menu():
    print(HELLO)
    while True:
        s = input().strip()
        if s.lower() == "exit":
            exit(0)
        if s.lower() == "start":
            return start()
        elif s.lower() == "bot":
            bot()
        elif len(s.split()) == 2 and s.split()[0].lower() == "load":
            f = load_field(s.split()[1])
            if f is None:
                print("Введите start/bot/load {filename}/exit")
                continue
            return f
        else:
            print("Ошибка. Введите start/bot/load {filename}/exit")


def start():
    print("Создаем поле n*m")
    n = get_num("Введите число n")
    while n <= 0:
        error()
        n = get_num("Введите число n")
    m = get_num("Введите число m")
    while m <= 0:
        error()
        m = get_num("Введите число m")
    bomb_min = get_num("Введите минимальное число бомб на карте(<=n*m; > 0)")
    while bomb_min <= 0 or bomb_min > n*m:
        error()
        bomb_min = get_num("Введите минимальное число бомб на карте(<=n*m; > 0)")
    bomb_max = get_num("Введите максимальное число бомб на карте(<n*m; >= минимального)")
    while bomb_max < bomb_min or bomb_max > n*m:
        error()
        bomb_max = get_num("Введите максимальное число бомб на карте(<n*m; >= минимального)")
    bomb_count = random.randint(bomb_min, bomb_max)
    return Field(n, m, get_bombs(n, m, bomb_count))

