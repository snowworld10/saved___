import json
import logging
import opentele
import datetime as dt
import multiprocessing
import shutil
from telethon.tl.types import ChannelParticipant

import random
from telethon.tl.functions.channels import GetFullChannelRequest
from opentele.td import TDesktop
from opentele.api import API, UseCurrentSession
import asyncio
import time
import os

async def main(tdata_folder, channel_username, interval, channel_limit, lock):
    final_output = set([])        
    tasks = []
    for i in range(1):
# Load TDesktop client from tdata folder
        connected = False
        while not connected:
            try:
                print('connecting')
                tdataFolder = fr"/home/ubuntu/notifications_bot/accounts_base/{random.choice(os.listdir('/home/ubuntu/notifications_bot/accounts_base'))}/tdata"
                with lock:
                    if not check_rest(tdataFolder.split("/")[-2]):
                        continue

                logger.info(tdataFolder)
                tdesk = TDesktop(tdataFolder)

        # Using official iOS API with randomly generated device info
        # print(api) to see more
                api = API.TelegramAndroid

        # Convert TDesktop session to telethon client
        # CreateNewSession flag will use the current existing session to
        # authorize the new client by `Login via QR code`.
                client = await tdesk.ToTelethon(flag=UseCurrentSession, api=api, password='112233')
                await client.connect()
                await client.get_entity('https://t.me/xtichkdydykiddt')
                connected = True
                with lock:
                    add_to_rest(tdataFolder.split("/")[-2])
            except Exception as exc:
                print(exc.args)
                if type(exc.args[0]) is not int and ('deactivated' in exc.args[0] or "not registered" in exc.args[0] or "file or directory" in exc.args[0]):
                    logger.info('exception')
                    try:        
                        d_folder = tdataFolder.split("/")[-2].split("/")[0]
                        logger.info(d_folder)
                        shutil.rmtree(tdataFolder.split("/tdata")[0])
                    except Exception as exc:
                        logger.info(exc.args)
            except opentele.exception.TFileNotFound:
                pass
        
        channel_connect = channel_username.split('/')[-1]
        channel_connect = channel_connect.split('@')[-1]
        try:
            channel_full_info = await client(GetFullChannelRequest(channel=channel_connect))
        except:
            return []
        participants_count = channel_full_info.full_chat.participants_count
        if participants_count < 10000 and i > 0:
            continue
        logger.info(f'connection number {i}')

        tasks.append(client.loop.create_task(get_users(client, channel_username, interval, channel_limit)))

    for task in tasks:
        res = await task
        if res == 'get_messages required':
            final_output = await get_messages(client, channel_username, interval)
            break
        else:
            [final_output.add(user) for user in res]

    return list(final_output)

async def get_messages(client, url, interval):

    result = []

    time.sleep(0.1)

    logger.info('getting messages')
    print(interval)

	# wait for a task to complet
    try:
        try:
            for coro in asyncio.as_completed([client.get_messages(url, limit=100000, offset_date=dt.datetime.now(tz=dt.timezone.utc) - dt.timedelta(days=interval),reverse=True)], timeout=300):
                messages = await coro
        except asyncio.TimeoutError:
            for coro in asyncio.as_completed([client.get_messages(url, limit=20000, offset_date=dt.datetime.now(tz=dt.timezone.utc) - dt.timedelta(days=interval),reverse=True)], timeout=300):
                messages = await coro
    except Exception as exc:
        logger.info(exc.args)
        logger.info(f'exception during finding messages {exc.args}')
        return []

    logger.info(messages)
    logger.info('got messages')
    print('got messages, return result')
    result = set([])

    try:
        admins = await client.get_participants(url)
    except Exception as exc:
        admins = []

    for message in messages:
        try:
            if not message.sender.bot and message.sender.username and message.sender not in admins:
                result.add(message.sender.username)
        except AttributeError:
            pass

    logger.info("return result")
    return list(result)

async def get_users(client, channel_username, interval, channel_limit):
    if not await _check_channel(client, channel_username, channel_limit):
        logger.info('channel is under filder returning []')
        return []

    result = []
    try:
        logger.info('get participants request')
        
        for coro in asyncio.as_completed([client.get_participants(channel_username)], timeout=900):
            users = await coro

        logger.info(users)
        if len(users) < 100:
            2 / 0
        for user in users:
           print('checking user')
           if not user.bot and type(user.participant) is ChannelParticipant and user.username and _check_date(user=user, interval=interval):
                print(user)
                result.append(user.username)
    except Exception as exc:
        logger.info(exc.args)
        print('getting messages required')
        return 'get_messages required'

    return result

def entry_point(links, conn_send, tdata_folder, interval, channel_limit, not_completed_queue, lock):
    result = []
    not_completed = 0

    logger.info(links)
    for link in links:
        logger.info('started getting process')
        try:
            result_part = asyncio.run(main(tdata_folder, link, interval, channel_limit, lock))
        except Exception as exc:
            print(exc.args)
        if result_part is None:
            result = None
            break
        elif not result_part:
            not_completed += 1
            logger.info(not_completed)
        else:
            [result.append(user) for user in result_part]

    conn_send.put(result)
    not_completed_queue.put(not_completed)

def _check_date(user=None, message=None, interval=None):

    if user:
        try:
            second_point = user.status.was_online
            print(user.status.was_online)
        except AttributeError:
            print('user was not online')
            return False
    else:
        second_point = message.date

    logger.info(second_point)

    first_point = dt.datetime.now(second_point.tzinfo) - dt.timedelta(days=interval)

    if second_point > first_point:
        return True
    else:
        logger.info(second_point)
        return  False

async def _check_channel(client, url, channel_limited):
    # 10 attempts to establish connection with api.telegram. If after 10 attempts it still raises error,
    # then there are connection problems or channel does not exist

    for _ in range(10):
        time.sleep(0.5)
        try:
            channel_connect = await client.get_entity(f'{url}') 
            channel_full_info = await client(GetFullChannelRequest(channel=channel_connect))
            participants_count = channel_full_info.full_chat.participants_count
            if channel_limited and participants_count > 100000:
                logger.info('channel is under filter')
                return False
            else:
                return True
        except Exception as exc:
            logger.info(exc.args)


    return False




def add_to_rest(session_file): 
    with open("rest.json", "r") as f: 
        rest_dict = json.loads(f.read())
    rest_dict[session_file] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("rest.json", "w") as f:
        f.write(json.dumps(rest_dict))

def check_rest(session_file): 
    with open("rest.json") as f: 
        rest_dict = json.loads(f.read())
    try: 
        date_rest = rest_dict[session_file] 
    except KeyError as exc: 
        return True
    date_rest = dt.datetime.strptime(date_rest, "%Y-%m-%d %H:%M:%S") 
    yesterday = dt.datetime.now() - dt.timedelta(days=1) 
    yesterday = yesterday.strftime("%Y-%m-%d %H:%M:%S") 
    yesterday = dt.datetime.strptime(yesterday, "%Y-%m-%d %H:%M:%S") 
    if yesterday > date_rest:
        return True 
    else: 
        logger.info("account cant be used because it is in rest")
        return False

logger = logging.getLogger('__main__')
logger.setLevel(logging.INFO)
logging.basicConfig(filename='log.txt', filemode='a')
