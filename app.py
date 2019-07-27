# server_simple.py
from aiohttp import web
import aiohttp
import asyncio
import aiohttp_jinja2
from aiohttp_jinja2 import jinja2
import signup_and_login as sign
import json

routes = web.RouteTableDef()

@routes.get('/mywallet')
@aiohttp_jinja2.template('mywallet.html')
async def handler1(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}


@routes.get('/detail')
@aiohttp_jinja2.template('detail.html')
async def handler2(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}


@routes.get('/signup')
@aiohttp_jinja2.template('signup.html')
async def handler3(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}


@routes.get('/netnode')
@aiohttp_jinja2.template('netnode.html')
async def handler4(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}

@routes.get('/introduce')
@aiohttp_jinja2.template('intro.html')
async def handler5(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}

@routes.post('/signup_emailcheck')
async def check_email(request):
    return web.Response(text=await sign.checkEmail(request))

@routes.post('/signup_signup')
async def signup(request):    
    return web.Response(text=await sign.signup(request))

@routes.post('/send_info_to')
async def handle_info(request):
    data = await request.post()
    """
    data description:
    * fabric client result:
        signup login query transfer etc.
    * connetcor result:
        server list search result
    * same type server message exchange    
    """

    return web.Response(text='1')

async def start_background_tasks(app):
    app['kickout'] = app['loop'].create_task(sign.kickout(app))

# async def cleanup_background_tasks(app):
#     print('into clean up')
#     app['kickout'].cancel()
#     await app['kickout']

@web.middleware
async def server_redirect(request, handler):    
    cookies = request.cookies
    print('server redirect s', ' the cookie is: ',cookies)    
    location = cookies.get('redirect')
    if location:
        raise web.HTTPFound('https://www.baidu.com')
    else:
        response = await handler(request)
        print('server redirect e')
        return response

async def init(app):
    """
    request connector to fetch info
    """
    with open('./config.json','r') as f:
        appinfo = json.load(f)
    for k in appinfo:
        app[k] = appinfo[k] 
    session = await aiohttp.ClientSession()
    for url in appinfo['connectors']: 
        if len(appinfo['require_type']) <=0:
            break
        nexturl = url.strip('/')+'/get_server/'
        for item in appinfo['require_type']:
            nexturl += item+'&'          
        async with session.get(nexturl) as resp:
            ans = await resp.text()
            print('request for connector answer ',ans)  
            try:
                ans = json.loads(ans)
                for item in appinfo['require_type']:
                    app[item] = ans[item]
                break                 
                pass
            except Exception:
                pass  
              
            
    session.close()

async def main(loop):
    app = web.Application(middlewares=[server_redirect])  
    app['loop']=loop  
    await init(app)
    app['emailcode'] = {}
    app.on_startup.append(start_background_tasks)
    # app.on_cleanup.append(cleanup_background_tasks)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./views'))    
    routes.static('/s', './public', append_version=True)
    app.add_routes(routes)      
    runner = web.AppRunner(app)    
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', app['port'])
    await site.start()
    await asyncio.sleep(99999999999)

import sys
if sys.platform == 'win32':
    loop = asyncio.ProactorEventLoop()
else:
    loop = asyncio.get_event_loop()
        
asyncio.set_event_loop(loop)
try:
    loop.run_until_complete(main(loop))
except KeyboardInterrupt:
    pass
loop.close()