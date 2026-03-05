import aiohttp

API = "https://west.albion-online-data.com/api/v2/stats/prices/"

async def get_price(item):

    async with aiohttp.ClientSession() as session:

        async with session.get(API + item) as r:

            data = await r.json()

            if not data:
                return None

            return data[0]["sell_price_min"]
