import asyncio
import os
from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv
from engine.engine import Engine


load_dotenv()

bot = AsyncTeleBot(os.getenv("TELEGRAM_TOKEN"))

engine = Engine(bot, os.getenv("API_TOKEN"))


@bot.message_handler(commands=['start'])
async def welcome(message):
    await engine.welcome(message)


@bot.message_handler(content_types=['text'])
async def handle_imei_check(message):
    await engine.handle_imei_check(message)



if __name__ == '__main__':
    asyncio.run(engine.main())