from itertools import cycle

alp = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def crypt_vijn(text, key):
    f = lambda arg: alp[(alp.index(arg[0])+alp.index(arg[1])%33)%33]
    return ''.join(map(f, zip(text, cycle(key))))


def decrypt_vijn(text, key):
    f = lambda arg: alp[alp.index(arg[0])-alp.index(arg[1])%33]
    return ''.join(map(f, zip(text, cycle(key))))
