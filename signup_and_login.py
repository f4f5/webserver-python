import asyncio
from email.mime.text import MIMEText
import aiosmtplib
import random
import time

async def sendMail(toaddress, ecode):    
    message = MIMEText("Sent via aiosmtplib")
    message["From"] = "root@localhost"
    message["To"] = toaddress
    message["Subject"] = "验证码"
    message.attach(MIMEText("验证码", "plain", "utf-8"))
    message.attach(MIMEText(F"<html><body><h1>验证码: {ecode}</h1></body></html>", "html", "utf-8"))

    async with aiosmtplib.SMTP(hostname="127.0.0.1", port=1025) as smtp:
        await smtp.auth_login(username='jass@qq.com',password='skj')
        await smtp.send_message(message)

async def checkEmail(request):    
    timenow = int(time.time())
    eaddress = request.body.email
    if request.app['emailcode'].get(eaddress):
        return '0'    
    ecode = str(random.randint(10000000, 99999999))
    ecode = ecode[-6:]
    signandlog.emailcode[eaddress] = [ecode,timenow]
    await sendMail(eaddress, ecode)
    return '1'

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
    data = await request.post()
    
    pass