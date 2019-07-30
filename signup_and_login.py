import asyncio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from aiohttp_session import get_session, new_session
import aiosmtplib
import random
import time
import re
import utils

async def sendMail(toaddress, ecode):    
    message = MIMEMultipart("alternative")
    message["From"] = "root@localhost"
    message["To"] = toaddress
    message["Subject"] = "验证码"
    message.attach(MIMEText("验证码", "plain", "utf-8"))
    message.attach(MIMEText(F"<html><body><h1>验证码: {ecode}</h1></body></html>", "html", "utf-8"))

    async with aiosmtplib.SMTP(hostname="127.0.0.1", port=1025) as smtp:
        await smtp.auth_login(username='jazz@qq.com',password='skj')
        await smtp.send_message(message)

async def checkEmail(request):    
    timenow = int(time.time())
    tmp = await request.post()
    eaddress = tmp.get('email')
    if request.app['emailcode'].get(eaddress):
        return '0'    
    ecode = str(random.randint(10000000, 99999999))
    ecode = ecode[-6:]
    request.app['emailcode'][eaddress] = [ecode,timenow]
    re_email=r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    if re.match(re_email, eaddress):
        await sendMail(eaddress, ecode)
        return '1'
    else:
        return '0'

async def kickout(app):
    timenow = int(time.time())
    print('first into kickout')
    while True:
        print('loop kick')
        for item in app['emailcode']:
            if timenow - app['emailcode'][item][1] > 172800000:
                del app['emailcode'][item]
        await asyncio.sleep(3600)
        
async def signup(request):
    """
    this function will do the folowing:
        1. request block chain to make sure the name unique
        2. request for new wallet from fabric
        3. store the user identity into levelDB
        4. send identity info to client
    """
    data = await request.post()
    sig = {'Password': data['inputPassword'], 'Address': data['inputAddress']}
    urls = request.app['fabric'].copy()
    signup_result = await utils.sureAnswer(urls, '/signup', sig)    
    # here deal with the signup_result to fit the page side
    return signup_result

async def login (request):
    #log in to fabric
    #creat session
    #store password or address to redes
    data = await request.post()
    logi = {'Password': data['inputPassword'], 'Address': data['inputAddress']}    
    urls = request.app['fabric'].copy()
    login_result = await utils.sureAnswer(urls,'/login', logi)
    session = await new_session(request)
    session['keepalive'] = login_result['login_hash']
    return login_result
    pass


