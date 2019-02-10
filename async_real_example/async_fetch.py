import time
import asyncio
from colorama import init as color_init, Fore, Back, Style
from tqdm import tqdm
from aiohttp import ClientSession, TCPConnector

# init colorama
color_init()

task_info = []


async def fetch(url, session, url_count):
    async with session.get(url) as response:
        c0 = f"start call {url_count}"
        c1 = f"complete call {url_count}"
        # print(Fore.RED + c0) # uncomment if you want to watch calls
        r = await response.json()
        # print(Fore.YELLOW + c1) # uncomment if you want to watch calls
        return r


async def run(r):
    tasks = []
    url_count = 1
    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    # for my test 150 was the optimal number
    conn = TCPConnector(limit=300)
    async with ClientSession(connector=conn) as session:
        for i in r:
            task = asyncio.ensure_future(fetch(i, session, url_count))
            tasks.append(task)
            url_count += 1

        bob = []
        for f in tqdm(
            asyncio.as_completed(tasks),
            total=len(tasks),
            desc="Async Calls",
            unit=" request",
        ):
            bob.append(await f)

        responses = await asyncio.gather(*tasks)

        # you now have all response bodies in this variable
        # print_responses(responses)
        return responses


def print_responses(result):
    # print(result)
    for x in result:
        print(f"Task Name: {x['name']} created at {x['created']}")


def async_fetch(task_url):
    t0 = time.time()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(task_url))
    obj = loop.run_until_complete(future)
    # loop.close()
    t1 = time.time() - t0
    # print(int(t1))

    return obj


# if __name__ == '__main__':
#     main()
