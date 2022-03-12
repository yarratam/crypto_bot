from itertools import cycle

alp = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
alp_upper = alp.upper()


def crypt_char(arg):
    a = alp if arg[0].islower() else alp_upper
    return a[(a.index(arg[0])+a.index(arg[1])%33)%33]


def decrypt_char(arg):
    a = alp if arg[0].islower() else alp_upper
    return a[a.index(arg[0])-a.index(arg[1])%33]


def crypt_vijn(text, key):
    return ''.join(map(crypt_char, zip(text, cycle(key))))


def decrypt_vijn(text, key):
    return ''.join(map(decrypt_char, zip(text, cycle(key))))
