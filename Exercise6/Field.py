from lib import *
from encryption import encrypt, decrypt


class Field(object):
    def __init__(self, rows, cols, bombs, user_matrix=None, flags=None):
        self._rows = rows
        self._cols = cols
        self._bombs = bombs
        if flags is None:
            self._flags = []
        else:
            self._flags = flags
        self._real_matrix = get_matrix(rows, cols, self._bombs)
        if user_matrix is None:
            self._user_matrix = []
            for i in range(rows):
                self._user_matrix.append(['x'] * cols)
        else:
            self._user_matrix = user_matrix

    def get_flags_count(self):
        return len(self._flags)

    def get_bombs_count(self):
        return len(self._bombs)

    def get_size(self):
        return [self._rows, self._cols]

    def get_flags(self):
        return self._flags

    def get_bombs(self):
        return self._bombs

    def get_field(self):
        return self._user_matrix

    def print_field(self):
        print(f"Flags: {len(self._flags)}/{len(self._bombs)}")
        if self._cols < 1000 and self._rows < 100:
            print('\t', end='')
            for i in range(self._cols):
                print(str(i + 1), end='\t')
            print('\n', end='\t')
            for i in range(self._cols):
                print('‾', end='\t')
            print('')
            for i in range(self._rows):
                print(str(i + 1) + '|', end='\t')
                for j in range(self._cols):
                    print(self._user_matrix[i][j], end='\t')
                print('')
        else:
            for i in range(self._rows):
                for j in range(self._cols):
                    print(self._user_matrix[i][j], end='')
                print('')

    def change_flag(self, x, y):
        if x < 1 or x > self._rows or y < 1 or y > self._cols:
            return
        if self._user_matrix[x-1][y-1] == 'f':
            self._flags.remove([x, y])
            self._user_matrix[x-1][y-1] = 'x'
        else:
            self._flags.append([x, y])
            self._user_matrix[x-1][y-1] = 'f'

    def clear_flags(self):
        for i in range(self._rows):
            for j in range(self._cols):
                if self._user_matrix[i][j] == 'f':
                    self._user_matrix[i][j] = 'x'
        self._flags = []

    def is_win(self):
        if sorted(self.get_flags()) == sorted(self.get_bombs()):
            for i in range(self._rows):
                for j in range(self._cols):
                    if self._user_matrix[i][j] != 'x':
                        return True
        else:
            return False

    def open_nulls(self, x, y):
        if self._real_matrix[x - 1][y - 1] == 0 and self._user_matrix != 'f':
            self._user_matrix[x - 1][y - 1] = '0'
        for_iterate = []
        for_open = []
        f = True
        for_iterate.append([x, y])
        while f:
            f = False
            iter_lst = for_iterate
            for_iterate = []
            for x, y in iter_lst:
                for i in range(x - 1, x + 2):
                    for j in range(y - 1, y + 2):
                        if is_in_range(i, 1, self._rows) and is_in_range(j, 1, self._cols):
                            if [i, j] not in for_open and [i, j] not in self._bombs:
                                for_open.append([i, j])
                                if self._real_matrix[i-1][j-1] == 0:
                                    for_iterate.append([i, j])
                                    f = True
        for i, j in for_open:
            if self._user_matrix[i-1][j-1] != 'f':
                self._user_matrix[i-1][j-1] = chr(self._real_matrix[i-1][j-1] + ord('0'))

    def open(self, x, y):
        if x < 1 or x > self._rows or y < 1 or y > self._cols:
            return True
        if [x, y] in self._bombs:
            self._user_matrix[x-1][y-1] = 'B'
            return False
        else:
            if self._real_matrix[x-1][y-1] == 0:
                if self._user_matrix[x-1][y-1] == 'x':
                    self.open_nulls(x, y)
            else:
                self._user_matrix[x-1][y-1] = chr(self._real_matrix[x-1][y-1] + ord('0'))
            return True

    def save(self, file):
        f = open(file, 'w')
        lst = encrypt(self._bombs, self._rows + self._cols / 2)
        for n in lst:
            f.write(str(int(n)) + ' ')
        f.write('\n')
        for i in range(self._rows):
            for j in range(self._cols):
                f.write(self._user_matrix[i][j])
            f.write('\n')
        f.close()
        print(f"Файл {file} сохранен.")
