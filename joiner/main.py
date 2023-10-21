import time
import multiprocessing
import json
import telethon_tools as tt
import asyncio

def joiner(quantity, url, order_id):
    asyncio.run(joiner_wrapper(quantity, url, order_id))

async def joiner_wrapper(quantity, url, order_id):
    lock = asyncio.Lock()
    tasks = set()
    [tasks.add(asyncio.create_task(tt.init_connection(url, order_id, lock))) for _ in range(quantity)]

    order_info = {"url": url, "quantity": quantity, "id": order_id, "accounts": []}

    with open(f"/home/ubuntu/joiner/orders/{order_id}.json", "w") as f:
        f.write(json.dumps(order_info))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    checking_process = multiprocessing.Process(target=tt.status_online_mp_wrapper)
    checking_process.start()
    checking_process.kill()
    multiprocessing.Process(target=joiner, args=(3, "iopkes", "3002",)).start()
    time.sleep(300)
    checking_process = multiprocessing.Process(target=tt.status_online_mp_wrapper)
    checking_process.start()
