import asyncio

import aiohttp
import requests
# import bs4
from colorama import Fore
import csv
import datetime
from unsync import unsync
from dotenv import load_dotenv
import os

load_dotenv()


loop = asyncio.get_event_loop()

async def get_response(zip_code: int) -> str:
    print(Fore.YELLOW + f"Getting weather for {zip_code}", flush=True)

    # url = f'https://talkpython.fm/{episode_number}'
    api_key = os.getenv("API_KEY")
    api_key = '59fd897708e64f6743d65b0f47879f72'
    country = 'us'
    url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip_code},us&appid={api_key}"
    # resp = requests.get(url)
    # data = resp.json()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                temp = 'not available'
            else:
                resp.raise_for_status()
                data = resp.json()
                main_group = data['main']
                value = main_group['temp']
                y = 273.15
                f = (float(value) - 273.15) * 9 / 5 + 32
                temp = int(round(f))
                print(Fore.BLUE + f"The tempature in {zip_code} is {temp}F", flush=True)
            return await temp

    # if resp.status_code != 200:
    #     temp = 'not available'
    # else:
    #     resp.raise_for_status()
    #     data = resp.json()
    #     main_group = data['main']
    #     value = main_group['temp']
    #     y = 273.15
    #     f = (float(value) - 273.15) * 9/5 + 32
    #     temp = int(round(f))
    #     print(Fore.BLUE + f"The tempature in {zip_code} is {temp}F", flush=True)

    # return temp



def get_zip_list():
    zc = []
    with open('zc.csv', newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=' ')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                # print(', '.join(row))
                zc.append(int(row[0]))
                line_count += 1
        print(f'Processed {line_count} lines.')
    return zc


def main():
    # What am I fetching?
    t0 = datetime.datetime.now()
    zc = get_zip_list()
    print(zc)

    loop.run_until_complete(get_zip_range(zc))
    #x = get_zip_range(zc)
    loop.close()
    dt = datetime.datetime.now() - t0
    print("Synchronous version done in {:,.2f} seconds.".format(dt.total_seconds()))
    return



async def get_zip_range(zc):
    z = zc
    print(f"z = {z}")

    tasks = [(n, loop.create_task(get_response(n)))
             for n in z
             ]

    for t in tasks:
            te = await t
            print(Fore.WHITE + f"Temp found: {te}", flush=True)
    # tasks = [
    #     (n, loop.create_task(get_response(n)))
    #     for n in z
    # ]
    # for t in tasks:
    #     te = await t
    #     print(Fore.WHITE + f"Temp found: {te}", flush=True)


if __name__ == '__main__':
    main()
