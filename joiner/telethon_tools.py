import datetime as dt
from telethon import functions
from telethon.tl.functions.account import UpdateStatusRequest
import asyncio
import time
from settings import logger
import os
from opentele.tl import TelegramClient
from opentele.api import APIData, API
import random
import json
proxy = {'proxy_type': 'http', 'addr': 'geo.iproyal.com', 'port': 12321, 'username': 'sanshao', 'password': '994620715_streaming-1'}

async def init_connection(url, order_id, lock, return_client=False):
    joined = False
    while not joined:
        while True:
            if return_client:
                account_info_fn = return_client + ".json"
            else:
                account_info_fn = random.choice(os.listdir('/home/ubuntu/joiner/accounts_base')) 
            if 'json' in account_info_fn:
                acc_info = get_acc_info(account_info_fn)
                if acc_info is not None:
                    print(acc_info)
                    break
                elif return_client:
                    return None

        api = APIData(api_id=int(acc_info["app_id"]), api_hash=acc_info["app_hash"],
        device_model=acc_info["device"], app_version=acc_info["app_version"], system_lang_code=acc_info["system_lang_pack"], lang_pack=acc_info["lang_pack"])
    # do some things
        try:
            if return_client:
                client = TelegramClient(f"/home/ubuntu/joiner/accounts_base/{return_client}.session", api=api, proxy=proxy)
            else:
                client = TelegramClient(session=f'/home/ubuntu/joiner/accounts_base/{acc_info["session_file"]}.session', api=api, proxy=proxy)
            if return_client:
                await client.connect()
                await client.get_entity("BotFather")
                return client
            async with lock:
                await client.connect()
                await client.get_entity("BotFather")
                await asyncio.sleep(0.5)
            break            
        except Exception as exc:
            try:
                await client.disconnect()
            except:
                pass
            print(exc.args)
            if "deactivated" in exc.args[0] or "not registered" in exc.args[0] or "was used under two" in exc.args[0]:
                print("removing")
                
                try:
                    await client.disconnect()
                except:
                    pass

                os.system(f'rm /home/ubuntu/joiner/accounts_base/{acc_info["session_file"]}.session')
                os.remove(f'/home/ubuntu/joiner/accounts_base/{acc_info["session_file"]}.json')
                if return_client:
                    return None
            elif return_client:
                return False
        time.sleep(1)
    #add_to_rest(acc_info["session_file"])

        logger.info("connected, joining") 
    
        time.sleep(random.randint(0,60))
        try:
            res = await client(functions.channels.JoinChannelRequest( 
                            channel=url
                    ))
            joined = True 
        except Exception as exc:
            logger.info(f"exception during joining {exc.args}")
            continue

    logger.info("joined")
    
    async with lock:
        with open(f"/home/ubuntu/joiner/orders/{order_id}.json") as f:
            order_dict = json.loads(f.read())
        order_dict["accounts"].append(acc_info["session_file"])

        with open(f"/home/ubuntu/joiner/orders/{order_id}.json", "w") as f:
            f.write(json.dumps(order_dict))

async def status_online_wrapper():
    logger.info("status online wrapper started")
    tasks = [] 
    lock = asyncio.Lock()
    for order_fn in os.listdir("/home/ubuntu/joiner/orders"):
        tasks.append(status_online(order_fn, lock))
    
    await asyncio.gather(*tasks)

async def status_online(order_fn, lock):
    with open(f"/home/ubuntu/joiner/orders/{order_fn}") as f:
        order_info = json.loads(f.read())
    acc_to_remove = []
  
    while True:  
        for session_file in order_info["accounts"]:
            logger.info("getting client by filename")
            client = await init_connection(url=order_info["url"], order_id=order_info["id"], lock=lock, return_client=session_file)
            logger.info("got client")
            if client is None:
                acc_to_remove.append(session_file)
                break
            elif client == False:
                continue

            try:
                await client(UpdateStatusRequest(offline=False))
                logger.info("status updated")
            except Exception as exc:
                logger.info(f"exception during status update {exc.args}")
            
            if not check_cancelled(order_info["id"]):
                try:
                    os.remove(f"/home/ubuntu/joiner/orders/{order_fn}")
                except:
                    pass
                finally:
                    return
       
        if acc_to_remove:
            [order_info["accounts"].remove(acc) for acc in acc_to_remove]
            acc_to_remove = []
            with open(f"/home/ubuntu/joiner/orders/{order_fn}", "w") as f:
                f.write(json.dumps(order_info))

def status_online_mp_wrapper():
    asyncio.run(status_online_wrapper())

def check_cancelled(order_id):
    return True

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
        s.logger.info("account cant be used because it is in rest")
        return False
        

def get_acc_info(filename):
    try:
        with open(f'/home/ubuntu/joiner/accounts_base/{filename}', 'r') as f:
            return json.loads(f.read())
    except Exception as exc:
        return None


