import time
import requests
from async_real_example.async_fetch import async_fetch
from async_real_example.async_post import async_post

def get_task_list(url):
    task_list = []
    r = requests.get(url)

    if r.status_code != 200:
        task_list = f"service error of {r.status_code} encountered."
    else:
        x = r.json()
        for i in x:
            print(f"ID: {i['id']}")
            id = f"{url}{i['id']}"
            task_list.append(id)
            task_list.append(id)
            task_list.append(id)
            task_list.append(id)
            task_list.append(id)
            task_list.append(id)
            task_list.append(id)
            task_list.append(id)
            task_list.append(id)
            task_list.append(id)
            task_list.append(id)
            task_list.append(id)
            task_list.append(id)
            task_list.append(id)
            task_list.append(id)
            task_list.append(id)
            task_list.append(id)
            task_list.append(id)
            task_list.append(id)
            task_list.append(id)
            task_list.append(id)
            task_list.append(id)
            task_list.append(id)
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
    # What am I fetching?
    t_start = time.time()
    # call API
    url = "https://learning-camunda.devsetgo.com/rest/engine/default/task/"
    task_url = get_task_list(url)
    print(len(task_url))
    # print(task_url)
    # call async_1
    
    # task_url = []
    # for a in range(0,30):
    #     task_url.append("http://www.fakeresponse.com/api/?sleep=1")


    t_start_sync = time.time()
    print(f"Starting sync test")
    result_sync = sync_test(task_url)
    t_duration_sync = time.time() - t_start_sync
    print(f'The sync process took {int(t_duration_sync)} seconds to complete.')

    t_start_async = time.time()
    print(f"Starting async test")
    result_async = async_fetch(task_url)
    t_duration_async = time.time() - t_start_async
    print(f'The async process took {int(t_duration_async)} seconds to complete.')
    # duration calc
    t_duration = time.time() - t_start
    print(f'The process took {t_duration} to complete.')
    t_faster = t_duration_sync - t_duration_async
    print(f"How much faster is Async? {t_faster} seconds or {int(t_duration_sync / t_duration_async)} times faster")

    return


if __name__ == '__main__':
    main()
