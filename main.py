from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters
from caesar import encrypt_caesar, decrypt_caesar
from vijn import crypt_vijn, decrypt_vijn


TOKEN = '5022929800:AAGP058VrDbt3c44xJGfASE8rUIL52eY0G8'

user_storage = {}

CRYPT_TITLES = {
    'cez': 'Шифр Цезаря',
    'vij': 'Шифр Виженера'
}


def get_start_markup():
    markup_values = (
        ('Шифр Цезаря', 'start_cez'),
        ('Шифр Вижинера', 'start_vij')
    )
    buttons = [InlineKeyboardButton(c, callback_data=cb) for c, cb in markup_values]
    markup = InlineKeyboardMarkup([buttons])
    return markup


def method_choose_handler(update: Update, key):
    markup_values = (
        ('Зашифровать', f'choose_{key}_crypt'),
        ('Расшифровать', f'choose_{key}_decrypt')
    )
    buttons = [InlineKeyboardButton(c, callback_data=cb) for c, cb in markup_values]
    markup = InlineKeyboardMarkup([buttons])
    update.callback_query.message.reply_text(f'Выбран {CRYPT_TITLES[key]}', reply_markup=markup)


def choose_crypt_or_decrypt(update: Update, key, method):
    if key == 'cez':
        user_storage[update.effective_user.id] = {
            'step': 'shift',
            'key': key,
            'method': method
        }
        return update.callback_query.message.reply_text('Выберите сдвиг')
    if key == 'vij':
        user_storage[update.effective_user.id] = {
            'step': 'key_input',
            'key': key,
            'method': method
        }
        return update.callback_query.message.reply_text('Введите ключ')


def start(update: Update, ctx: CallbackContext):
    update.message.reply_text('Выберите шифр:', reply_markup=get_start_markup())


def button_handler(update: Update, ctx):
    query_data = update.callback_query.data
    update.callback_query.answer()
    cb_data = query_data.split('_')
    route = cb_data[0]
    if route == 'start':
        return method_choose_handler(update, cb_data[1])
    elif route == 'choose':
        return choose_crypt_or_decrypt(update, cb_data[1], cb_data[-1])


def text_handler(update: Update, ctx):
    conf = user_storage.get(update.effective_user.id)
    if not conf:
        print('user not found')
        return
    key = conf['key']
    step = conf['step']
    if step == 'final':
        return crypt(update)
    if key == 'cez':
        if step == 'shift':
            return select_shift_handler(update)
    if key == 'vij':
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
    if key == 'cez':
        shift = int(conf['shift'])
        answer = encrypt_caesar(message, shift) if method == 'crypt' else decrypt_caesar(message, shift)
    if key == 'vij':
        crypt_key = conf['crypt_key']
        answer = crypt_vijn(message, crypt_key) if method == 'crypt' else decrypt_vijn(message, crypt_key)
    update.message.reply_text(answer)


def run_bot():
    updater = Updater(TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button_handler))
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=text_handler))
    updater.start_polling()
    updater.idle()


run_bot()
