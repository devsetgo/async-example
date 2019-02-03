import time
import requests
from async_real_example.async_fetch import async_fetch

def get_task_list(url):
    task_list = []
    r = requests.get(url)

    if r.status_code != 200:
        task_list.append(f"service error of {r.status_code} encountered.")
    else:
        x = r.json()
        for i in x:
            # print(f"ID: {i['id']}")
            id = f"{url}{i['id']}"

            # loop through to extend the amount of calls
            for b in range(0, 100):
                task_list.append(id)

    return task_list

def sync_test(task_url):
    result = []
    c = 1
    for e in task_url:

        r = requests.get(e)
        print(c)
        c += 1
        result.append(r.json())

    return result

def main():
    # start the clock
    t_start = time.time()
    # call API
    url = "https://learning-camunda.devsetgo.com/rest/engine/default/task/"
    task_url = get_task_list(url)
    print(len(task_url))

    # call async_1
    print(f"There are {len(task_url)} tasks to be called.")
    # t_start_sync = time.time()
    # print(f"Starting sync test")
    # result_sync = sync_test(task_url)
    # t_duration_sync = time.time() - t_start_sync
    # rate_sync = len(task_url) / t_duration_sync
    # print(f'The sync process took {t_duration_sync} seconds to complete at a rate of ~{rate_sync} calls per seconds.')

    t_start_async = time.time()
    print(f"Starting async test")
    result_async = async_fetch(task_url)
    t_duration_async = time.time() - t_start_async
    rate_async = len(task_url) / t_duration_async
    print(f'The async process took {t_duration_async} seconds to complete at a rate of {rate_async} calls per seconds.')

    # duration calc
    t_duration = time.time() - t_start
    print(f'The entire test took {t_duration} seconds to complete')
    # t_faster = t_duration_sync - t_duration_async
    # print(f"How much faster is Async? {t_faster} seconds or {t_duration_sync / t_duration_async} times faster and {rate_async - rate_sync} calls per second faster")

    return


if __name__ == '__main__':
    main()
