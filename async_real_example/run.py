import time
import requests

from tqdm import tqdm, trange
from async_fetch import async_fetch


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
            for b in range(0, 1000):
                task_list.append(id)

    return task_list


def sync_test(task_url):
    result = []
    c = 1
    for e in tqdm(task_url, desc="Sync Calls", unit=" request", total=len(task_url)):
        r = requests.get(e)
        # print(c)
        c += 1
        result.append(r.json())

    return result


def main():
    # Change this to set a limit on how many Sync calls to make during the test.
    sync_test_threshold = 100
    # start the clock
    t_start = time.time()
    # call API
    url = "https://learning-camunda.devsetgo.com/rest/engine/default/task/"
    task_url = get_task_list(url)
    # print(f"There are {len(task_url)} tasks to fetch")
    if len(task_url) < sync_test_threshold:

        # call async_1
        print(f"There are {len(task_url)} tasks to fetch")
        # print(f"There are {len(task_url)} tasks to be called.")
        t_start_sync = time.time()
        print(f"Starting sync test")
        result_sync = sync_test(task_url)
        t_duration_sync = time.time() - t_start_sync
        rate_sync = len(task_url) / t_duration_sync
        print(
            f"The sync process took {t_duration_sync:.2f} seconds to complete at a rate of ~{rate_sync:.2f} calls per seconds."
        )

        t_start_async = time.time()
        print(f"Starting async test")
        result_async = async_fetch(task_url)
        t_duration_async = time.time() - t_start_async
        rate_async = len(task_url) / t_duration_async
        print(
            f"The async process took {t_duration_async:.2f} seconds to complete at a rate of {rate_async:.2f} calls per seconds."
        )
        print(len(result_async))
        # duration calc
        t_duration = time.time() - t_start
        print(f"The entire test took {t_duration:.2f} seconds to complete")
        t_faster = t_duration_sync - t_duration_async
        print(
            f"How much faster is Async? {t_faster:.2f} seconds or {(t_duration_sync / t_duration_async):.2f} times faster and {(rate_async - rate_sync):.2f} calls per second faster"
        )
    else:
        print(
            f"Over Test Threshold of {sync_test_threshold} and will only proceed wth Async Test and fetch {len(task_url)} tasks"
        )
        t_start_async = time.time()
        print(f"Starting async test")
        result_async = async_fetch(task_url)
        t_duration_async = time.time() - t_start_async
        rate_async = len(task_url) / t_duration_async
        print(
            f"The async process took {t_duration_async:.2f} seconds to complete at a rate of {rate_async:.2f} calls per seconds."
        )
        # print(f"Process Results = {len(result_async)}")
    return


if __name__ == "__main__":
    main()
