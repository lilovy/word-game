import logging
import os
from aiogram import Bot, Dispatcher, executor, types
# from aioredis import Redis
from dotenv import load_dotenv, find_dotenv
from tg_game import game, last_ltr
from temp_storage import fill_dict, buffer_user, buffer_bot, user_bases
from db_connection import db
from datetime import datetime


# from dictionary_word import return_word


load_dotenv(find_dotenv())

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)
adminId = 347265373

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends '/start' or '/help' command
    """
    if message.chat.id != db.select_user(message.chat.id)[0]:
        db.insert_user(message.chat.id, message.chat.username)
    await message.reply("""Hi!\nIt's word-game
                        by @anggel_s
                        for start game /newgame""")


@dp.message_handler(commands=['newgame'])
async def newgame(message: types.Message):
    if message.chat.id != db.select_user(message.chat.id)[0]:
        db.insert_user(message.chat.id, message.chat.username)

    bot_word = game()
    db.insert_game(message.chat.id)
    db.insert_bot_buff(message.chat.id, bot_word)
    await message.reply(bot_word)


@dp.message_handler(commands=['buffer'])
async def returnbuff(message: types.Message):
    await message.reply(db.select_user_buff(message.chat.id))


@dp.message_handler(commands=['allbuffer'])
async def buffall(message: types.Message):
    if message.chat.id == adminId:
        db_buffer = [(frame[0], frame[1].strip(), frame[2], frame[3].isoformat(' ')) for frame in db.select_all_userbuff()]
        await message.reply(db_buffer)
    else:
        await message.reply('internal command')


@dp.message_handler(commands=['users'])
async def printusers(message: types.Message):
    if message.chat.id == adminId:
        users_db = [(frame[0], frame[1].strip(), frame[2].isoformat(' ')) for frame in db.select_all_users()]
        await message.reply(users_db)
    else:
        await message.reply('internal command')


@dp.message_handler(commands=['allgames'])
async def printgames(message: types.Message):
    if message.chat.id == adminId:
        db_games = [(frame[0], frame[2], frame[1].isoformat(' ')) for frame in db.select_all_games()]
        await message.reply(db_games)
    else:
        await message.reply('internal command')


@dp.message_handler(commands=['faults'])
async def printfault(message: types.Message):
    if message.chat.id == adminId:
        db_fauls = [(frame[0], frame[1].strip(), frame[2], frame[3].isoformat(' ')) for frame in db.select_all_faults()]
        await message.reply(db_fauls)
    else:
        await message.reply('internal command')


@dp.message_handler(commands=['addword'])
async def addword():
    ...


# @dp.message_handler(commands=['newgame'])
# async def newgame():
#     ...


@dp.message_handler()
async def echo(message: types.Message):
    if message.chat.id != db.select_user(message.chat.id)[0]:
        db.insert_user(message.chat.id, message.chat.username)

    slowo = message.text.lower()

    try:
        if slowo in db.select_user_buff()[-1][0]:   # check client word in buffer for not repeat
            await message.answer('word used later, input new word')
        else:
            db.insert_user_buff(message.chat.id, slowo)
    except Exception as ex:
        db.insert_user_buff(message.chat.id, slowo)

    word_bot = db.select_bot_buff(message.chat.id)[-1][0].strip()      # return last word in bot buffer
    # if word_bot
    last_l = last_ltr(word_bot)                     # return last letter in word_bot or penultimate if last letter in ('ь', '.', 'ы')

    if slowo[0] == last_l:                          # check first letter in client word and last letter in bot word
        w_bot = game(slowo)
        if w_bot:
            db.insert_bot_buff(message.chat.id, w_bot)
            await message.answer(w_bot)
        else:
            await message.answer('incorrect word')
            db.del_word(message.chat.id, slowo)
            db.select_user_fault(message.chat.id)
            await message.answer(db.select_bot_buff(message.chat.id)[-1][0].strip())
    else:
        db.del_word(message.chat.id, slowo)
        db.select_user_fault(message.chat.id)
        await message.answer('incorrect word')
        await message.answer(db.select_bot_buff(message.chat.id)[-1][0].strip())

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
