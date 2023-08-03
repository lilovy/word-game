from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='/newgame'),
            KeyboardButton(text='/help'),
        ]
    ]
)

reply_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='recall a word'),
            KeyboardButton(text='search in wikipedia'),
            KeyboardButton(text='/buffer'),
        ],
        [
            KeyboardButton(text='/help'),
            KeyboardButton(text='/newgame'),
            KeyboardButton(text='admin command'),
        ]
    ], one_time_keyboard=False)

admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='/users'),
        KeyboardButton(text='/allbuffer'),
        KeyboardButton(text='/faults'),
    ],
    [
        KeyboardButton(text='go back')
    ]
], resize_keyboard=True)
