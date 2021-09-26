
from lib import *
import math


def permutation(word, rule_to, rule_from=None):
    if rule_from is None:
        rule_from = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    rt = 0
    for ch in str(word):
        for i in range(len(rule_from)):
            if ch == str(rule_from[i]):
                if rt == 0:
                    rt += rule_to[i]
                else:
                    rt *= 10
                    rt += rule_to[i]
    return rt


def lst_permutation(lst, rule_to, rule_from=None):
    rt = []
    for n in lst:
        rt.append(permutation(n, rule_to, rule_from))
    return rt


def fib_shift_encrypt(nums, k=5):
    """
    начинаю считать числа Фиббиначи с k, и для каждого числа из nums использую формулу
    rs = k^2 * num^2 + 11*fib*num^2 + num^2*k*fib^3 + num^2*fib_old^3,
    num - число для шифрования, fib - число Фиббаначи для нынешней итерации,
    fib_old - для прошлой, k=кол-во строк * кол-во стобцов/2 матрицы.
    """
    fib_old_old = 0
    fib = k
    rt = []
    for num in nums:
        fib_old = fib
        fib += fib_old_old
        rs = k**2 * num**2 + 11*fib*num**2 + num**2*k*fib**3 + num**2*fib_old**3
        rt.append(rs)
        fib_old_old = fib_old
    return rt


def fib_shift_decrypt(nums, k=5):
    fib_old_old = 0
    fib = k
    rt = []
    for num in nums:
        fib_old = fib
        fib += fib_old_old
        rs = round(math.sqrt(num/(k**2 + 11*fib + k*fib**3 + fib_old**3)))
        rt.append(rs)
        fib_old_old = fib_old
    return rt


def encrypt(bombs, k):
    k = round(k)
    rule = [0, 6, 4, 3, 2, 8, 1, 7, 5, 9]
    new_bombs = []
    for x, y in bombs:
        new_bombs.append(x)
        new_bombs.append(y)
    new_bombs = lst_permutation(new_bombs, rule)
    new_bombs = fib_shift_encrypt(new_bombs, k)
    return new_bombs


def decrypt(bombs, k):
    k = round(k)
    rule = [0, 6, 4, 3, 2, 8, 1, 7, 5, 9]
    enc_bombs = fib_shift_decrypt(bombs, k)
    enc_bombs = lst_permutation(enc_bombs, rule)
    rt = []
    for i in range(0, len(enc_bombs) - 1, 2):
        rt.append([enc_bombs[i], enc_bombs[i+1]])
    return rt
