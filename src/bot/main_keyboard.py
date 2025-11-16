from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Создать привычку'),
            KeyboardButton(text='Мои привычки'),
        ],
        [
            KeyboardButton(text='Выполнить привычку'),
            KeyboardButton(text='Статистика'),
        ],
    ],
    resize_keyboard=True
)