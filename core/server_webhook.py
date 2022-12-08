import logging
import os
from aiogram import Bot, types
from aiogram.dispatcher.filters import Text

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook

from dotenv import load_dotenv, find_dotenv
from core.tg_game import game, last_ltr
from core.keyboards.reply import reply_keyboard, admin_keyboard, start_keyboard
from db_control.db_manipulation import (create_record,
                                        check_word,
                                        check_user,
                                        get_items,
                                         check_game,
                                        check_buffer,
                                        get_user,
                                        del_record,
                                        get_word,
                                        )
from db_control.db_models.users import Users
from db_control.db_models.user_buffer import UsersBuffer
from db_control.db_models.bot_buffer import BotBuffer
from db_control.db_models.user_fault import UsersFault
from db_control.db_models.games import Games
from db_control.db_models.users_words import UserDict


load_dotenv(find_dotenv())

logging.basicConfig(level=logging.INFO)


# webhook settings
WEBHOOK_HOST = os.getenv('HOST')
WEBHOOK_PATH = os.getenv('API')
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = os.getenv('APP')  # or ip
WEBAPP_PORT = 3001


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)
adminId = int(os.getenv('ANDMINID'))
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends '/start' or '/help' command
    """
    check_user(message.chat.id, message.chat.username)

    return SendMessage("Простая игра в слова с ботом\n"
                        "by @anggel_s\n"
                        ""
                        "to launch a game: /newgame", reply_markup=start_keyboard)


@dp.message_handler(commands='help')
async def help_command(message: types.Message):
    return SendMessage("Классическая игра в слова:\n"
                        "напиши слово начинающееся на\n"
                        "последнюю букву слова оппонета")


@dp.message_handler(Text(equals='admin command'))
async def admin_command(message: types.Message):
    if message.chat.id == adminId:
        return SendMessage("admin commands:", reply_markup=admin_keyboard)
    else:
        return SendMessage("access restricted")


@dp.message_handler(Text(equals=['go back']))
async def go_back_command(message: types.Message):
    return SendMessage("user commands", reply_markup=reply_keyboard)


@dp.message_handler(Text(equals='recall a word'))
async def go_back_command(message: types.Message):
    return SendMessage(get_word(BotBuffer,
                                  userId=message.chat.id) +
                         f""" - {last_ltr(get_word(BotBuffer,
                                                   userId=message.chat.id,
                                                   game=check_game(message.chat.id)))}""")


@dp.message_handler(commands=['newgame'])
async def newgame(message: types.Message):

    check_user(message.chat.id, message.chat.username)
    gm = check_game(message.chat.id)

    if gm == 0:
        create_record(Games,
                      userId=message.chat.id,
                      game=1)
    create_record(Games,
                  userId=message.chat.id,
                  game=gm + 1)

    bot_word = game()

    create_record(BotBuffer,
                  userId=message.chat.id,
                  word=bot_word,
                  game=gm + 1)

    return SendMessage(bot_word +
                        f""" - {last_ltr(get_word(BotBuffer, 
                                                  userId=message.chat.id, 
                                                  game=check_game(message.chat.id)))}""",
                        reply_markup=reply_keyboard)


@dp.message_handler(commands=['buffer'])
async def returnbuff(message: types.Message):
    return SendMessage(check_buffer(UsersBuffer,
                                     userId=message.chat.id,
                                     game=check_game(message.chat.id)))

    # ----------------------------- #
    #        admin commands         #
    # ----------------------------- #


@dp.message_handler(commands=['allbuffer'])
async def buffall(message: types.Message):

    if message.chat.id == adminId:
        return SendMessage(check_buffer(UsersBuffer))

    else:
        return SendMessage('access restricted')


@dp.message_handler(commands=['users'])
async def printusers(message: types.Message):

    if message.chat.id == adminId:
        return SendMessage(get_user())

    else:
        return SendMessage('access restricted')


# @dp.message_handler(commands=['allgames'])
# async def printgames(message: types.Message):
#     if message.chat.id == adminId:
#         db_games = [(frame[0], frame[2], frame[1].isoformat(' ')) for frame in db.select_all_games()]
#         await message.reply(db_games)
#     else:
#         await message.reply('internal command')


@dp.message_handler(commands=['faults'])
async def printfault(message: types.Message):

    if message.chat.id == adminId:
        return SendMessage(check_buffer(UsersFault))

    else:
        return SendMessage('access restricted')

    # -----------------------------------------


@dp.message_handler(commands=['addword'])
async def addword(message: types.Message):
    ...


@dp.message_handler(Text(equals=''))


@dp.message_handler()
async def echo(message: types.Message):

    check_user(userId=message.chat.id,
               name=message.chat.username)

    slowo = message.text.lower()

    try:
        if check_word(UsersBuffer,
                      userId=message.chat.id,
                      word=slowo,
                      game=check_game(message.chat.id)):

            return SendMessage('word used later, input new word\n',
                               get_word(BotBuffer,
                                        userId=message.chat.id) +
                                 f""" - {last_ltr(get_word(BotBuffer, 
                                                           userId=message.chat.id, 
                                                           game=check_game(message.chat.id)))}""")

        else:
            create_record(UsersBuffer,
                          userId=message.chat.id,
                          word=slowo,
                          game=check_game(message.chat.id))

            word_bot = get_word(BotBuffer,
                                userId=message.chat.id,
                                game=check_game(message.chat.id))

            last_l = last_ltr(word_bot)  # return last letter in word_bot or penultimate
                                         # if last letter in ('ь', '.', 'ы')

            if slowo[0] == last_l:       # check first letter in client word and last letter in bot word
                w_bot = game(slowo)
                if w_bot:
                    create_record(BotBuffer,
                                  userId=message.chat.id,
                                  word=w_bot,
                                  game=check_game(message.chat.id))
                    return SendMessage(w_bot +
                                         f""" - {last_ltr(get_word(BotBuffer, 
                                                                   userId=message.chat.id, 
                                                                   game=check_game(message.chat.id)))}""")

                else:
                    del_record(UsersBuffer,
                               userId=message.chat.id,
                               word=slowo,
                               game=check_game(message.chat.id))

                    create_record(UsersFault,
                                  userId=message.chat.id,
                                  word=slowo,
                                  game=check_game(message.chat.id))

                    return SendMessage('incorrect word, check the word you typed\n',
                                       get_word(BotBuffer,
                                                userId=message.chat.id) +
                                         f""" - {last_ltr(get_word(BotBuffer,
                                                                   userId=message.chat.id,
                                                                   game=check_game(message.chat.id)))}""")

            else:
                del_record(UsersBuffer,
                           userId=message.chat.id,
                           word=slowo,
                           game=message.chat.id)

                create_record(UsersFault,
                              userId=message.chat.id,
                              word=slowo,
                              game=check_game(message.chat.id))

                return SendMessage(f"""incorrect word, input a word beginning with - 
                                           '{last_ltr(get_word(BotBuffer,
                                                               userId=message.chat.id,
                                                               game=check_game(message.chat.id)))}\n'""",
                                   get_word(BotBuffer,
                                            userId=message.chat.id) +
                                     f""" - {last_ltr(get_word(BotBuffer,
                                                               userId=message.chat.id,
                                                               game=check_game(message.chat.id)))}""")

    except:
        create_record(UsersBuffer,
                      userId=message.chat.id,
                      word=slowo,
                      game=check_game(message.chat.id))


async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown():
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


def main():
    # executor.start_polling(dp, skip_updates=True)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )


if __name__ == "__main__":
    main()
