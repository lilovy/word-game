import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv, find_dotenv
from core.tg_game import game, last_ltr, return_meaning
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


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)
adminId = int(os.getenv('ANDMINID'))


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends '/start' or '/help' command
    """
    check_user(message.chat.id, message.chat.username)

    await message.reply("Простая игра в слова с ботом\n"
                        "by @anggel_s\n"
                        ""
                        "to launch a game: /newgame", reply_markup=start_keyboard)


@dp.message_handler(commands='help')
async def help_command(message: types.Message):
    await message.reply("Классическая игра в слова:\n"
                        "напиши слово начинающееся на\n"
                        "последнюю букву слова оппонета")


@dp.message_handler(Text(equals='admin command'))
async def admin_command(message: types.Message):
    if message.chat.id == adminId:
        await message.reply("admin commands:", reply_markup=admin_keyboard)
    else:
        await message.answer("access restricted")


@dp.message_handler(Text(equals=['go back']))
async def go_back_command(message: types.Message):
    await message.reply("user commands", reply_markup=reply_keyboard)


@dp.message_handler(Text(equals='recall a word'))
async def go_back_command(message: types.Message):
    await message.answer(get_word(BotBuffer,
                                  userId=message.chat.id) +
                         f""" - {last_ltr(get_word(BotBuffer,
                                                   userId=message.chat.id,
                                                   game=check_game(message.chat.id)))}""")


@dp.message_handler(Text(equals='search in wikipedia'))
async def word_meaning(message: types.Message):
    await message.answer(return_meaning(get_word(BotBuffer, userId=message.chat.id)))


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

    await message.reply(bot_word +
                        f""" - {last_ltr(get_word(BotBuffer, 
                                                  userId=message.chat.id, 
                                                  game=check_game(message.chat.id)))}""",
                        reply_markup=reply_keyboard)


@dp.message_handler(commands=['buffer'])
async def returnbuff(message: types.Message):
    await message.reply(check_buffer(UsersBuffer,
                                     userId=message.chat.id,
                                     game=check_game(message.chat.id)))

    # ----------------------------- #
    #        admin commands         #
    # ----------------------------- #


@dp.message_handler(commands=['allbuffer'])
async def buffall(message: types.Message):

    if message.chat.id == adminId:
        await message.reply(check_buffer(UsersBuffer))

    else:
        await message.reply('access restricted')


@dp.message_handler(commands=['users'])
async def printusers(message: types.Message):

    if message.chat.id == adminId:
        await message.reply(get_user())

    else:
        await message.reply('access restricted')


@dp.message_handler(commands=['faults'])
async def printfault(message: types.Message):

    if message.chat.id == adminId:
        await message.reply(check_buffer(UsersFault))

    else:
        await message.reply('access restricted')

    # -----------------------------------------


# @dp.message_handler(commands=['addword'])
# async def addword(message: types.Message):
#     ...


# @dp.message_handler(Text(equals=''))


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

            await message.answer('word used later, input new word')
            await message.answer(get_word(BotBuffer,
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
                    await message.answer(w_bot +
                                         f""" - {last_ltr(get_word(BotBuffer, 
                                                                   userId=message.chat.id, 
                                                                   game=check_game(message.chat.id)))}""")

                else:
                    await message.answer('incorrect word, check the word you typed')

                    del_record(UsersBuffer,
                               userId=message.chat.id,
                               word=slowo,
                               game=check_game(message.chat.id))

                    create_record(UsersFault,
                                  userId=message.chat.id,
                                  word=slowo,
                                  game=check_game(message.chat.id))

                    await message.answer(get_word(BotBuffer,
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

                await message.answer(f"""incorrect word, input a word beginning with - 
                                           '{last_ltr(get_word(BotBuffer,
                                                               userId=message.chat.id,
                                                               game=check_game(message.chat.id)))}'""")
                await message.answer(get_word(BotBuffer,
                                              userId=message.chat.id) +
                                     f""" - {last_ltr(get_word(BotBuffer,
                                                               userId=message.chat.id,
                                                               game=check_game(message.chat.id)))}""")

    except:
        create_record(UsersBuffer,
                      userId=message.chat.id,
                      word=slowo,
                      game=check_game(message.chat.id))


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
