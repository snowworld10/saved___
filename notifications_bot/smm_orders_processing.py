import datetime
import os
import shutil
import time
import asyncio
from opentele.td import TDesktop
from opentele.api import API, UseCurrentSession
import traceback

import telebot
import multiprocessing
import settings as s
import requests as r
import smm_engine as engine
import random
from telethon.tl.types import ChannelParticipant
from telethon import events
from telethon import TelegramClient

lock = multiprocessing.Lock()

def orders_checking():		
    old_orders = []
    while True:
        time.sleep(30)
        telebot_instance = telebot.TeleBot(s.token[1])
        old_telebot_instance = telebot.TeleBot(s.token[0])
        if len(os.listdir('/home/ubuntu/notifications_bot/accounts_base')) < 25:
            telebot_instance.send_message(s.admin_user_id, '用于履行订单的帐户已用完！')
            old_telebot_instance.send_message(s.admin_user_id, '用于履行订单的帐户已用完！')
            time.sleep(600)
        else:
            bot_folders = []
            for _ in range(25):
                bot_folders.append(random.choice(os.listdir('accounts_base')))
            id_list = [1013,812,813]
            orders_list = []
            statuses = ["in_progress", "processing", "pending"]

            for status in statuses:
                req = r.get(f'https://db-laren.com/adminapi/v2/orders?apikey=um3qln1eabpa0zdltmmfyydcqdtk6ygqzc6okebs4r89jq6qxqzoiyaazmudbipa&service_ids=812,813,1013&order_status={status}')
                req = req.json()
                [orders_list.append(order) for order in req["data"]["list"]]
                
            for order in orders_list:
                    id = int(order["service_id"])
#                res = {'status': 'success', 'link': 't.me/xtichkdydykiddt', 'comments': 'https://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858\r\nhttps://t.me/Zhenjiang8858', 'id': '159'}
                    if id == 812:
                        channel_limit = True
                        print('channel_limit is True')
                    else:
                        print('channel limit is False')
                        channel_limit = False

                    res = r.get(f'https://db-laren.com/adminapi/v2/orders/{order["id"]}?apikey=um3qln1eabpa0zdltmmfyydcqdtk6ygqzc6okebs4r89jq6qxqzoiyaazmudbipa')
                    res = res.json()
                    oid = res["data"]["id"]
                    try:
                        res = res["data"]
                        res["comments"] = res["order_buttons"]["comment"]
                        links = res["comments"]
                    except Exception as exc:
                        logger.info(exc.args)
                        continue
                    if res["id"] in old_orders:
                        continue
                    engine.logger.info(f'Found new order with type {id}')
                    old_orders.append(res["id"])
                    p = multiprocessing.Process(target=wrapper_1, args=(links, bot_folders, channel_limit, res, id,lock,))                    
                    p.start()
                    

      









def wrapper_1(links, bot_folders, channel_limit, res, id, lock):
    try:
        engine.logger.info("wrapper 1 opened")
        print("wrapper 1 opened")
        if id in [812,813]:
            asyncio.run(process_812_order(links, bot_folders, channel_limit, res, lock))
        elif id == 1013:
            asyncio.run(find_groups(links,res["id"],res["link"]))
    except:
        traceback.print_exc()
        r.get(f'https://db-laren.com/adminapi/v1?key={s.smm_panel_api_token}&action=setCanceled&id={res["id"]}')

async def process_812_order(links, tdata_folders, channel_limit, res, lock):
    engine.logger.info("wrapper 2 opened")
    await process_812_order_(links, tdata_folders, channel_limit, res, lock)

async def find_groups(links,id, owner_link):
    engine.logger.info("wrapper 2 opened")
    await find_groups_(links,id, owner_link)

async def find_groups_(links,id, owner_link):
    global client
    engine.logger.info(links)        
    
    client = await _init_connection()

    bot_channel = await client.get_entity('@hao1234bot')
    await client.send_message(bot_channel, '/start')
    time.sleep(1)
    final_output = set([])
    not_completed = len(links)

    await client.send_message(bot_channel, '/language') 
    time.sleep(1) 
    message = await client.get_messages(bot_channel, limit=1) 
    message = message[0] 
    await message.click(0,1)
    time.sleep(1)

    for link in links:
        engine.logger.info(final_output)

        await client.send_message(bot_channel, link)
        time.sleep(1)

        message = await client.get_messages(bot_channel, limit=1)
        message = message[0]

        found = False
        if message.buttons is not None:
            for raw in message.buttons:
                for button in raw:
                    if '👥' in  button.text:
                        await button.click()
                        goal = int(button.text.split('(')[1][:-1])
                        found = True
        if not found:
            continue
       
        not_completed -= 1
        r.get(f'https://db-laren.com/adminapi/v1?key={s.smm_panel_api_token}&action=setRemains&id={id}&remains={not_completed}')
        print('success')

        message = await client.get_messages(bot_channel, limit=1)
        message = message[0]
        print(message.text)
        result_raw = message.text.split('\n\n')[1] 
        result_raw = result_raw.split('\n')
        [final_output.add(link.split('(')[-1][:-1]) for link in result_raw]
        print(final_output)
       
        try: 
            await message.click(4,1)
        except IndexError as exc:
            continue 

        for _ in range(500):
            message = await client.get_messages(bot_channel, limit=1)
            message = message[0]
            engine.logger.info(message.text)
            result_raw = message.text.split('\n\n')[1]
            result_raw = result_raw.split('\n')
            [final_output.add(link.split('(')[-1][:-1]) for link in result_raw]
            try:
                message.buttons[3][1]
            except:
                break

            client.loop.create_task(message.click(3,1))

            time.sleep(0.5)

    owner_profile = owner_link.split('/')[-1]
    owner_profile = owner_profile.split('@')[-1]
    final_output = list(final_output)
    if owner_profile not in os.listdir(f'/home/ubuntu/notifications_bot/ready_orders'):
        os.mkdir(f'/home/ubuntu/notifications_bot/ready_orders/{owner_profile}')
    with open(f'/home/ubuntu/notifications_bot/ready_orders/{owner_profile}/{id}','w') as f:
        [f.write(link + '\n') for link in final_output]

    engine.logger.info(not_completed)
    if not_completed == len(links):
        r.get(f'https://db-laren.com/adminapi/v1?key={s.smm_panel_api_token}&action=setCanceled&id={id}')
    elif not not_completed:
        r.get(f'https://db-laren.com/adminapi/v1?key={s.smm_panel_api_token}&action=setCompleted&id={id}')
    else:
        res = r.get(f'https://db-laren.com/adminapi/v1?key={s.smm_panel_api_token}&action=setPartial&id={id}&remains={not_completed}')
        print(res.json())

async def process_812_order_(links, tdata_folders, channel_limit, res, lock):
    try:
        interval = int(links[-1])
        links.remove(links[-1])
    except:
        interval = 30

    owner_profile = res["link"].split('/')[-1]
    owner_profile = owner_profile.split('@')[-1]
    finished = start_order_checking_thread(links, tdata_folders=tdata_folders, interval=interval, channel_limit = channel_limit, order_id=res["id"], lock=lock)
    if owner_profile not in os.listdir('/home/ubuntu/notifications_bot/ready_orders'):
        os.mkdir(f'/home/ubuntu/notifications_bot/ready_orders/{owner_profile}') 
    if finished is not None and finished:
        with open(f'/home/ubuntu/notifications_bot/ready_orders/{owner_profile}/{res["id"]}', 'w') as f:
            f.write('\n'.join(finished))

def start_order_checking_thread(links, tdata_folders, interval,channel_limit, order_id, lock):
    result = []
    queue = multiprocessing.Queue()
    not_completed_queue = multiprocessing.Queue() 
    not_completed = 0
    queue_num = 25
         
    print('starting_child_processes') 
    smm_engines = []
    if len(links) > 25: 
        first_index = len(links) // queue_num 
        for i in range(2, queue_num): 
            smm_engine = multiprocessing.Process(target=engine.entry_point,args=(links[first_index * i: first_index * (i + 1)], queue, random.choice(tdata_folders), interval, channel_limit, not_completed_queue, lock)) 
            smm_engines.append(smm_engine)
             
        smm_engines.append(multiprocessing.Process(target=engine.entry_point, 
        args=(links[:first_index], queue, random.choice(tdata_folders), 
        interval, channel_limit, not_completed_queue, lock))) 
        smm_engines.append(multiprocessing.Process(target=engine.entry_point, 
        args=(links[first_index * queue_num - 1:], queue, 
        random.choice(tdata_folders), interval, channel_limit, 
        not_completed_queue, lock)))
        for eng in smm_engines:
            eng.start()    
    else:

        smm_engine_1 = multiprocessing.Process(target=engine.entry_point,
                                               args=(links, queue, tdata_folders[0], interval, channel_limit, not_completed_queue, lock))

        smm_engines.append(smm_engine_1)        
        smm_engine_1.start()

    print('started collecting data')

    completed = 0
    for process in smm_engines:
        engine.logger.info('getting result')
        try:
            result_part = queue.get(timeout=3600)
            not_completed += not_completed_queue.get(timeout=3600)
        except Exception as exc:
            not_completed += (len(links) // len(smm_engines))
            continue
        engine.logger.info('got result')

        if result_part is None:
            result = None
            break
        [result.append(username) for username in result_part]
        if result_part:
            completed += (len(links) // len(smm_engines))
            res = r.get(f'https://db-laren.com/adminapi/v1?key={s.smm_panel_api_token}&action=setRemains&id={order_id}&remains={len(links) - completed}')
            print(res.json())           

    engine.logger.info('joining processes')

    for process in smm_engines:
        process.kill()

    if len(links) > not_completed > 0:
        r.get(f'https://db-laren.com/adminapi/v1?key={s.smm_panel_api_token}&action=setPartial&id={order_id}&remains={not_completed}')
    elif not_completed == len(links) or result is None:
        r.get(f'https://db-laren.com/adminapi/v1?key={s.smm_panel_api_token}&action=setCanceled&id={order_id}')
    elif not_completed == 0:
        r.get(f'https://db-laren.com/adminapi/v1?key={s.smm_panel_api_token}&action=setCompleted&id={order_id}')

    engine.logger.info('returning result')
    engine.logger.info(result)

    return result

async def _init_connection():
    connected = False 
    while not connected:
        try: 
            print('connecting') 
            tdataFolder = fr'/home/ubuntu/notifications_bot/accounts_base/{random.choice(os.listdir("/home/ubuntu/notifications_bot/accounts_base"))}/tdata' 
            print(tdataFolder)
            tdesk = TDesktop(tdataFolder)
       #Using official iOS API with randomly generated device info
        # print(api) to see more
            api = API.TelegramAndroid
        # Convert TDesktop session to telethon client CreateNewSession 
        # flag will use the current existing session to authorize the 
        # new client by `Login via QR code`.
            client = await tdesk.ToTelethon(flag=UseCurrentSession, api=api,password='112233')
            await client.connect()
            await client.get_entity('https://t.me/xtichkdydykiddt')
            connected = True
        except Exception as exc:
            print(exc.args)
            if os.path.exists(tdataFolder):
                shutil.rmtree(tdataFolder.split('/tdata')[0])
    return client




































