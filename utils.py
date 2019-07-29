import aiohttp
import json

async def post(url, data):
    session = await aiohttp.ClientSession()      
    async with session.post(url, data) as resp:
        ans = await resp.text()
        try:            
            return json.loads(ans)
            pass
        except Exception:
            pass
    await session.close()

async def get(url):
    session = await aiohttp.ClientSession()      
    async with session.post(url) as resp:
        ans = await resp.text()
        try:            
            return json.loads(ans)
            pass
        except Exception:
            pass
    await session.close()