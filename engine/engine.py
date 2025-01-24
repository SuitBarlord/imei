import asyncio
from async_requests.async_requests import RequestsTask
import json

class Engine(RequestsTask):
    def __init__(self, bot, api_token):
        self.bot = bot
        self.api_token = api_token

    
    async def welcome(self, message):
        await self.bot.send_message(message.chat.id, "Добро пожаловать! Отправьте IMEI для проверки.")
    
    async def __check_imei(self, imei):

        data = {
            "deviceId": str(imei),
            "serviceId": 1
            }
        
        headers = {
            "Accept": "application/json",
            'Authorization': 'Bearer ' + self.api_token,
            }

        result = await self.async_fetch_post('https://api.imeicheck.net/v1/checks', data, headers)

        if result['message']:
            info = f"Ошибка: {result['message']}"
            

        else:
            result = result["properties"]
            info = f''' Название девайса: {result['deviceName']},
                        Модель: {result['modelDesc']},
                        Страна: {result['purchaseCountry']}
                        ...
            '''

        return info


    async def handle_imei_check(self, message):
        imei = message.text.strip()
        if len(imei) != 15 or not imei.isdigit():
            await self.bot.send_message(message.chat.id, "Некорректный IMEI. IMEI должен состоять из 15 цифр.")
            return

        result = await self.__check_imei(imei)
        print(result)

        await self.bot.send_message(message.chat.id, f"Результаты проверки IMEI:\n{result}")

    
    async def main(self):
        await self.bot.polling(timeout=40, non_stop=True, request_timeout=90)

    