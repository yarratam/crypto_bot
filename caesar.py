from string import ascii_lowercase

alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

ALPHABET = ('абвгдеёжзиклмнопрстуфхчшщъыьэюя'
            'АБВГДЕЁЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')


def encrypt_caesar(text, shift):
    encrypted_alphabet = ALPHABET[shift:] + ALPHABET[:shift]
    encrypted = []
    for char in text:
        index = get_char_index(char, ALPHABET)
        encrypted_char = encrypted_alphabet[index] if index >= 0 else char
        encrypted.append(encrypted_char)
    return ''.join(encrypted)


def get_char_index(char, alphabet):
    char_index = alphabet.find(char)
    return char_index


def decrypt_caesar(msg, offset=None):
    encrypted_alphabet = ALPHABET[offset:] + ALPHABET[:offset]
    decrypted = []
    if offset:
        for char in msg:
            index = get_char_index(char, encrypted_alphabet)
            encrypted_char = encrypted_alphabet[index - offset] \
                if index >= 0 else char
            decrypted.append(encrypted_char)
        return ''.join(decrypted)