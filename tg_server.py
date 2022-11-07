import logging
from aiogram import Bot, Dispatcher, executor, types
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends '/start' or '/help' command
    """
    await message.reply("Hi!\nIt's word-game\n by Anggels")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
