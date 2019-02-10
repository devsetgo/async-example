# async-example
Trying to learn a bit about async

Some of this works, some doesn't. 

## Async Real Example
This will run a sync vs async test. I find it interesting to see how fast calls are comparing. 

run aysnc_real_example run.py to execute test


### Config settings
- 'sync_test_threshold' in run.py sets the maximum number of sync calls, before the test skips to async only testing
- Change url = "https://learning-camunda.devsetgo.com/rest/engine/default/task/" to whatever your url is.
  - please do not hit my server in anythin more than a very limited capacity or I will lock it out.
  - This API is fairly fast, but is not meant for your testing
- get_task_list() has a sub loop to add extra calls to amp up test. Change the range if your data is limited and you are trying for a higher number of calls.
