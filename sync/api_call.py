import aiohttp
import requests
# import bs4
from colorama import Fore
import csv
import datetime
from dotenv import load_dotenv
import os

load_dotenv()



def get_response(zip_code: int) -> str:
    print(Fore.YELLOW + f"Getting weather for {zip_code}", flush=True)

    # url = f'https://talkpython.fm/{episode_number}'
    api_key =  api_key = os.getenv("API_KEY")
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
        print(Fore.YELLOW + f"The tempature in {zip_code} is {temp}F", flush=True)

    return temp


def main():
    # What am I fetching?
    t_start = datetime.datetime.now()
    get_zip_range()

    t_end = datetime.datetime.now()
    t_duration = t_end - t_start
    print(f'The process took {t_duration} to complete.')
    print('Done')
    return


def get_zip_range():
    # Please keep this range pretty small to not DDoS my site. ;)
    # list = [33761,33762,33763,33764,33765,33766,33767]
    # for n in list:
    #     t = get_response(n)
    #     # zip_code = get_zipcode(html, n)
    #     print(Fore.WHITE + f"Temp found: {t}", flush=True)
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

    for n in zc:
        print(n)
        zip_code = n
        t = get_response(zip_code)
        # zip_code = get_zipcode(html, n)
        print(Fore.WHITE + f"Temp found: {t}", flush=True)


if __name__ == '__main__':
    main()
