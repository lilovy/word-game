import logging
import os
from aiogram import Bot, Dispatcher, executor, types
# from aioredis import Redis
from dotenv import load_dotenv, find_dotenv
from tg_game import game
from temp_storage import fill_dict, buffer_user, buffer_bot, user_bases

# from dictionary_word import return_word


load_dotenv(find_dotenv())

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends '/start' or '/help' command
    """
    if message.chat.id not in user_bases:
        fill_dict(message.chat.id, message.chat.username, user_bases)
    await message.reply("""Hi!\nIt's word-game
                        by @anggel_s
                        for start game /newgame""")


@dp.message_handler(commands=['newgame'])
async def newgame(message: types.Message):
    if message.chat.id not in user_bases:
        fill_dict(message.chat.id, message.chat.username, user_bases)

    buffer_bot.clear()
    buffer_user.clear()
    fill_dict(message.chat.id, game(), buffer_bot)
    await message.reply(buffer_bot[message.chat.id][-1])


@dp.message_handler(commands=['buff'])
async def returnbuff(message: types.Message):
    await message.reply(buffer_user[message.chat.id])


@dp.message_handler(commands=['buffall'])
async def buffall(message: types.Message):
    await message.reply(buffer_user)


@dp.message_handler(commands=['users'])
async def printusers(message: types.Message):
    await message.reply(user_bases)


@dp.message_handler(commands=['addword'])
async def addword():
    ...


# @dp.message_handler(commands=['newgame'])
# async def newgame():
#     ...


@dp.message_handler()
async def echo(message: types.Message):
    slowo = message.text.lower()
    if message.chat.id not in user_bases:
        fill_dict(message.chat.id, message.chat.username, user_bases)

    try:
        if slowo in buffer_user[message.chat.id]:
            await message.answer('word used later, input new word')
        else:
            fill_dict(message.chat.id, slowo, buffer_user)

    except:
        fill_dict(message.chat.id, slowo, buffer_user)
    if slowo[0] == buffer_bot[message.chat.id][-1][-1]:
        w_bot = game(slowo)
        if w_bot:
            fill_dict(message.chat.id, w_bot, buffer_bot)
            await message.answer(w_bot)
        else:
            await message.answer('incorrect word')
            await message.answer(buffer_bot[message.chat.id][-1])
    else:
        set(buffer_user[message.chat.id]).discard(slowo)
        await message.answer('incorrect word')
        await message.answer(buffer_bot[message.chat.id][-1])

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
