from Field import Field
from data_parser import parse_action
from menu import menu


def win(field: Field):
    field.print_field()
    print("Поздравляю, Вы победили!")
    exit(0)


def dead(field: Field):
    field.print_field()
    print("Вы проиграли.")
    exit(0)


def game_cycle(field: Field):
    while True:
        print("(X Y Open/Flag)/(save {filename})/(exit)")
        user_input = input().strip()
        x, y, f = parse_action(user_input, field)
        if f == 0:
            continue
        if f == 1:
            field.change_flag(x, y)
            if field.is_win():
                win(field)
        if f == 2:
            if not field.open(x, y):
                dead(field)
            if field.is_win():
                win(field)
        field.print_field()


def main():
    field = menu()
    field.print_field()
    game_cycle(field)


if __name__ == '__main__':
    main()
