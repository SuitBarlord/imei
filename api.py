from quart import Quart, jsonify, request
import json
from async_requests.async_requests import RequestsTask
from dotenv import load_dotenv
import os
load_dotenv()
# Тут использовал Quart, так как в отличии от flask имеет асинхрон
# так как изначально планировал все делать в асинхроне
app = Quart(__name__)
# наследует RequestTask для асинк запросов
class MyAPI(RequestsTask):
    def __init__(self, api_token):
        self.api_token = api_token
        self.headers = {
        'Authorization': 'Bearer ' + self.api_token,
        'Content-Type': 'application/json'
        }

    async def get_balance(self):
        external_data = await self.async_fetch_get('https://api.imeicheck.net/v1/account', self.headers)
        return jsonify(external_data)
    
    async def get_list_services(self):
        external_data = await self.async_fetch_get('https://api.imeicheck.net/v1/services', self.headers)
        return jsonify(external_data)
    
    async def check_imei(self, imei, service_id):
        data = {
            "deviceId": str(imei),
            "serviceId": int(service_id)
        }
        external_data = await self.async_fetch_post('https://api.imeicheck.net/v1/checks', data, self.headers)
        print(external_data)
        return jsonify(external_data)
    
    async def check_imeis(self, imeis:list, service_id):
        data = {
            "deviceIds": imeis,
            "serviceId": int(service_id),
            "duplicateProcessingType": "reprocess"
        }
        external_data = await self.async_fetch_post('https://api.imeicheck.net/v1/orders', data, self.headers)
        return jsonify(external_data)
    
    async def check_history(self):
        external_data = await self.async_fetch_get('https://api.imeicheck.net/v1/checks', self.headers)
        return jsonify(external_data)
    

    
    
my_api_instance = MyAPI(os.getenv("API_TOKEN"))

@app.route('/get-balance', methods=['GET'])
async def handle_get_balance():
    return await my_api_instance.get_balance()

@app.route('/get-services', methods=['GET'])
async def handle_get_list_services():
    return await my_api_instance.get_list_services()

@app.route('/check-imei', methods=['POST'])
async def handle_get_check_imei():
    data = await request.data
    # Декодируем байтовую строку в обычную строку
    decoded_string = data.decode('utf-8')

    # Парсим строку как JSON
    parsed_data = json.loads(decoded_string)

    # Извлекаем значение IMEI
    imei = parsed_data.get("imei")
    service_id = parsed_data.get("service_id")
    return await my_api_instance.check_imei(imei, service_id)

@app.route('/check-imeis', methods=['POST'])
async def handle_get_check_imeis():
    data = await request.data
    decoded_string = data.decode('utf-8')

    parsed_data = json.loads(decoded_string)

    service_id = parsed_data.get("service_id")
    imeis = [str(imei) for imei in parsed_data['imei']]
    return await my_api_instance.check_imeis(imeis, service_id)

@app.route('/check-history', methods=['GET'])
async def handle_get_check_history():
    return await my_api_instance.check_history()

if __name__ == '__main__':
    app.run()



