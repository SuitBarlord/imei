import asyncio
import os
from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv
from engine.engine import Engine

WHITE_LIST = []
load_dotenv()

bot = AsyncTeleBot(os.getenv("TELEGRAM_TOKEN"))

engine = Engine(bot, os.getenv("API_TOKEN"))


@bot.message_handler(commands=['start'])
async def welcome(message):
    await engine.welcome(message)


@bot.message_handler(content_types=['text'])
async def handle_imei_check(message):
    # Проверяем, есть ли пользователь в белом списке
    if message.from_user.id not in WHITE_LIST:
        bot.send_message(message.chat.id, "У вас нет доступа к этой команде.")
        return

    await engine.handle_imei_check(message)
    



if __name__ == '__main__':
    asyncio.run(engine.main())