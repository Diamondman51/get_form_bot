from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

registration_key = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Пройти регистрацию', callback_data='verify'), InlineKeyboardButton(text='Нет, не надо', callback_data='pass')],
])

phone_number_key = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Отправить номер телефона', request_contact=True)]
], resize_keyboard=True)

send_form = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отправить форму")]
], resize_keyboard=True)

send_loc = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Отправить локацию', request_location=True)]
], resize_keyboard=True)

admin_keyboards = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Получить все формы'), KeyboardButton(text="Получить формы по дате"), KeyboardButton(text='Получить локацию')]
], resize_keyboard=True)
