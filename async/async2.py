import datetime
import random
import asyncio
from aiohttp import ClientSession

async def fetch(url, session):
    async with session.get(url) as response:
        delay = response.headers.get("DELAY")
        date = response.headers.get("DATE")

        # print("{}:{} with delay {}".format(date, response.url, delay))
        return await response.json()


async def bound_fetch(sem, url, session):
    # Getter function with semaphore.
    async with sem:
        x = await fetch(url, session)
        print(f"Task Name: {x['name']} - {x['description']}")


async def run(r):
    t0 = datetime.datetime.now()
    url = "https://learning-camunda.devsetgo.com/rest/engine/default/task/1962bfdc-21e5-11e9-8e5d-0242ac11000d"
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(1000)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        for i in range(r):
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, url.format(i), session))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses
    dt = datetime.datetime.now() - t0
    print(f"Completed in {dt}")

    # print("Complete in {:,.2f} seconds.".format(dt.total_seconds()))

number = 10000
loop = asyncio.get_event_loop()

future = asyncio.ensure_future(run(number))
loop.run_until_complete(future)