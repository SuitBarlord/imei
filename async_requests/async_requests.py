import aiohttp
# Класс для асинк запросов
class RequestsTask():
    
    async def async_fetch_get(self, api_endpoint, headers):
        async with aiohttp.ClientSession() as session:
            async with session.get(api_endpoint, headers=headers, verify_ssl=False) as response:
                return await response.json()
            
    async def async_fetch_post(self, api_endpoint, data, headers):
        print(api_endpoint, data, headers)
        async with aiohttp.ClientSession() as session:
            async with session.post(api_endpoint, json=data, headers=headers, verify_ssl=False) as response:
                print(response)
                return await response.json()