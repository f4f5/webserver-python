import aiohttp
import json
import random

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

async def sureAnswer(urls, path, data=None):
    """ request until there is an answer
    ---
    `urls`: `List` url list waiting for requeste
    `path`: `str`  url tail for specific request
    `data`: `dict` if exist, the request method is post, otherwise get
    
    return:
        json
    """
    if len(urls)<=0:
        return {"code":500}
    url = random.choice(urls)
    if url.endswith('/'):
        url = url.strip('/')
    if not path.startswith('/'):
        path ='/'+path
    url += path
    if data:
        ans = await post(url, data)
    else:
        ans = await get(url)

    if not ans.get('result'):
        urls.remove(url)
        await sureAnswer(urls, path, data)
    else:
        return ans