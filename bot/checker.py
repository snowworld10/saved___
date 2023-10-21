import traceback
import os
import time
import json
from telethon.tl.functions.channels import GetFullChannelRequest
import telethon
import asyncio
import settings as s

async def log_in():
    try:
        os.remove("bot.session")
    except Exception as exc:
        traceback.print_exc()

    proxy = {"proxy_type": "http", "addr": "geo.iproyal.com", "port": 12321, "username": "sanshao", "password": "994620715_country-hk_streaming-1", "rdns": True}

    bot = await telethon.TelegramClient("bot", 24182188, "f2ba5137285373c1cff1d5f0f7da2109").start(bot_token=s.token)
    return bot

async def check(client):
    with open("settings.json") as f:
        sett = json.loads(f.read())
    
# = await bot(GetFullChannelRequest(sett["channel"]))
    members = await client.get_participants(int(sett["channel"][0]))
 
    members = [member.id for member in members]
    
    sett["allowed"] = members
    print(members)

    with open("settings.json", "w") as f:
        f.write(json.dumps(sett))

client = asyncio.run(log_in())
