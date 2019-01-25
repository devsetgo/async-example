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

def main():
    # What am I fetching?
    t0 = datetime.datetime.now()

    zip_codes = get_zip_range()
    #print(len(zip_codes))

    # print("data is", repr(zip_codes))
    tasks = []

    # for n in zip_codes:
    #     tasks.append(get_zip_range(n))


    print(tasks)
    [t.result() for t in tasks]

    dt = datetime.datetime.now() - t0
    print("Synchronous version done in {:,.2f} seconds.".format(dt.total_seconds()))
    return


@unsync()
def get_response(zip_code: int) -> str:
    print(Fore.YELLOW + f"Getting weather for {zip_code}", flush=True)

    # url = f'https://talkpython.fm/{episode_number}'
    api_key = os.getenv("API_KEY")
    country = 'us'
    url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip_code},us&appid={api_key}"
    resp = requests.get(url)

    if resp.status_code != 200:
        temp = 'not available'
    else:
        resp.raise_for_status()
        data = resp.json()
        main_group = data['main']
        value = main_group['temp']
        y = 273.15
        f = (float(value) - 273.15) * 9/5 + 32
        temp = int(round(f))
        print(Fore.BLUE + f"The tempature in {zip_code} is {temp}F", flush=True)

    return temp



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
        print(zc)
    return zc


def get_zip_range():
    # Please keep this range pretty small to not DDoS my site. ;)
    # list = [33761,33762,33763,33764,33765,33766,33767]
    # for n in list:
    #     t = get_response(n)
    #     # zip_code = get_zipcode(html, n)
    #     print(Fore.WHITE + f"Temp found: {t}", flush=True)
    zc = get_zip_list()
    print('Go!')#
    for n in zc:
        # print(n)
        zip_code = n
        t = get_response(zip_code)
        # zip_code = get_zipcode(html, n)
        #print(Fore.WHITE + f"Temp found: {t}", flush=True)


if __name__ == '__main__':
    main()
