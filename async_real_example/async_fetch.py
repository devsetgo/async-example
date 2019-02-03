import time
import asyncio
from aiohttp import ClientSession, TCPConnector

task_info = []



async def fetch(url, session):
    async with session.get(url) as response:
        # print(response.json())

        return await response.json()

async def run(r):
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    # for my test 150 was the optimal number
    conn = TCPConnector(limit=150)
    async with ClientSession(connector=conn) as session:
        for i in r:
            task = asyncio.ensure_future(fetch(i, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        # print_responses(responses)
        return responses

def print_responses(result):
    #print(result)
    for x in result:
        print(f"Task Name: {x['name']} created at {x['created']}")



def async_fetch(task_url):
    t0 = time.time()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(task_url))
    obj = loop.run_until_complete(future)
    loop.close()
    t1 = time.time() - t0
    # print(int(t1))

    return obj

# if __name__ == '__main__':
#     main()
