# server_simple.py
from aiohttp import web
import asyncio
import aiohttp_jinja2
from aiohttp_jinja2 import jinja2
import signup_and_login as sign
routes = web.RouteTableDef()

@routes.get('/mywallet')
@aiohttp_jinja2.template('mywallet.html')
async def handler(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}


@routes.get('/detail')
@aiohttp_jinja2.template('detail.html')
async def handler(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}


@routes.get('/signup')
@aiohttp_jinja2.template('signup.html')
async def handler(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}


@routes.get('/netnode')
@aiohttp_jinja2.template('netnode.html')
async def handler(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}

@routes.post('/signup_emailcheck')
async def check_email(request):
    return web.Response(text=await sign.checkEmail(request))

@routes.post('/signup_signup')
async def signup(request):    
    return web.Response(text=await sign.signup(request))

@routes.get('/introduce')
@aiohttp_jinja2.template('intro.html')
async def handler(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}

async def start_background_tasks(app):
    app['kickout'] = app['loop'].create_task(sign.kickout(app))

# async def cleanup_background_tasks(app):
#     print('into clean up')
#     app['kickout'].cancel()
#     await app['kickout']

async def main(loop):
    app = web.Application()  
    app['loop']=loop  
    app['emailcode'] = {}
    app.on_startup.append(start_background_tasks)
    # app.on_cleanup.append(cleanup_background_tasks)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./views'))    
    routes.static('/s', './public', append_version=True)    
    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
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