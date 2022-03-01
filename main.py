from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from caesar import encrypt_caesar, decrypt_caesar
from vijn import crypt_vijn, decrypt_vijn


TOKEN = '5022929800:AAGP058VrDbt3c44xJGfASE8rUIL52eY0G8'

user_storage = {}

CRYPT_TITLES = {
    'cez': 'Шифр Цезаря',
    'vij': 'Шифр Виженера'
}

CEZ = 'Шифр Цезаря'
VIJ = 'Шифр Виженера'

HELPS = {
    CEZ: 'Шифр Цезаря — это вид шифра подстановки, в котором каждый символ в открытом тексте заменяется символом, находящимся на некотором постоянном числе позиций левее или правее него в алфавите.',
    VIJ: 'Шифр Виженера - это метод шифрования алфавитного текста с использованием серии переплетённых шифров Цезаря , основанных на буквах ключевого слова. В нём используется форма полиалфавитной замены.'
}

start_button = KeyboardButton('/start')
default_markup = ReplyKeyboardMarkup([[start_button]])


def get_start_markup():
    # markup = ReplyKeyboardMarkup(markup_values)
    # buttons = [ReplyKeyboardMarkup(c, callback_data=cb) for c, cb in markup_values]
    buttons = [KeyboardButton(c) for c in (CEZ, VIJ)]
    markup = ReplyKeyboardMarkup([buttons, [start_button]])
    # markup = InlineKeyboardMarkup([buttons])
    return markup


def method_choose_handler(update: Update, key):
    print('choose')
    buttons = [KeyboardButton(c) for c in ('Зашифровать', 'Расшифровать')]
    markup = ReplyKeyboardMarkup([buttons, [start_button]], one_time_keyboard=True)
    user_storage[update.effective_user.id]['step'] = 'choosed'
    user_storage[update.effective_user.id]['key'] = update.message.text
    # update.message.reply_text('Выбран {name}'.format(name=key), reply_markup=markup)
    update.message.reply_text(HELPS[key], reply_markup=markup)


def choose_crypt_or_decrypt(update: Update, key, method):
    if key == CEZ:
        user_storage[update.effective_user.id] = {
            'step': 'shift',
            'key': key,
            'method': method
        }
        return update.message.reply_text('Выберите сдвиг')
    if key == VIJ:
        user_storage[update.effective_user.id] = {
            'step': 'key_input',
            'key': key,
            'method': method
        }
        return update.message.reply_text('Введите ключ')


def start(update: Update, ctx: CallbackContext):
    user_id = update.effective_user.id
    if user_id in user_storage:
        del user_storage[update.effective_user.id]
    update.message.reply_text('Выберите шифр:', reply_markup=get_start_markup())


def init_user_storage(update: Update):
    user_storage[update.effective_user.id] = {
        'step': 'start',
        'key': update.message.text,
        'method': None
    }


def text_handler(update: Update, ctx):
    print('mess', update.message)
    print('mess', update.inline_query)
    conf = user_storage.get(update.effective_user.id)
    message = update.message.text
    if not conf:
        print('user not found')
        init_user_storage(update)
        conf = user_storage[update.effective_user.id]
    key = conf['key']
    step = conf['step']
    if step == 'start' and message in (CEZ, VIJ):
        return method_choose_handler(update, key)
    if step == 'choosed' and message in ('Зашифровать', 'Расшифровать'):
        return choose_crypt_or_decrypt(update, key, message)
    if step == 'final':
        return crypt(update)
    if key == CEZ:
        if step == 'shift':
            return select_shift_handler(update)
    if key == VIJ:
        if step == 'key_input':
            return key_input_handler(update)
    print(update.message.text)
    print(user_storage.get(update.effective_user.id))


def select_shift_handler(update: Update):
    user_storage[update.effective_user.id]['step'] = 'final'
    user_storage[update.effective_user.id]['shift'] = update.message.text
    update.message.reply_text('Введите фразу для шифрования')


def key_input_handler(update: Update):
    user_storage[update.effective_user.id]['step'] = 'final'
    user_storage[update.effective_user.id]['crypt_key'] = update.message.text
    update.message.reply_text('Введите фразу для шифрования')


def crypt(update: Update):
    conf = user_storage.pop(update.effective_user.id)
    key = conf['key']
    message = update.message.text
    method = conf['method']
    answer = ''
    if key == CEZ:
        shift = int(conf['shift'])
        answer = encrypt_caesar(message, shift) if method == 'Зашифровать' else decrypt_caesar(message, shift)
    if key == VIJ:
        crypt_key = conf['crypt_key']
        answer = crypt_vijn(message, crypt_key) if method == 'Зашифровать' else decrypt_vijn(message, crypt_key)
    update.message.reply_text(answer, reply_markup=default_markup)


def choose_cez(*a):
    print('choose')
    print(*a)


def run_bot():
    updater = Updater(TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=text_handler))
    updater.start_polling()
    # updater.idle()


if __name__ == '__main__':
    run_bot()
