import aiohttp

API = "https://west.albion-online-data.com/api/v2/stats/prices/"

async def get_price(item):

    url = API + item

    async with aiohttp.ClientSession() as session:

        async with session.get(url) as r:

            data = await r.json()

            if not data:
                return None

            return data[0]["sell_price_min"]
